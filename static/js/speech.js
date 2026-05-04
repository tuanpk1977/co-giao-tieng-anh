(function () {
    const NO_TTS_MESSAGE = 'Máy này chưa hỗ trợ giọng đọc. Vui lòng mở bằng Chrome hoặc Edge, hoặc bật Google Text-to-Speech.';
    const NO_RECOGNITION_MESSAGE = 'Trình duyệt này chưa hỗ trợ nhận diện giọng nói. Vui lòng dùng Chrome hoặc Edge trên máy tính/Android.';
    const OPEN_BROWSER_MESSAGE = 'Bạn hãy mở bằng Chrome hoặc Edge để dùng chức năng nghe/nói.';
    const NEED_MIC_MESSAGE = 'Bạn chưa cấp quyền micro. Hãy bấm biểu tượng ổ khóa trên trình duyệt và Allow Microphone.';
    const NEED_SECURE_CONTEXT_MESSAGE = 'Micro chỉ hoạt động trên HTTPS hoặc localhost.';
    const WEBVIEW_MESSAGE = 'Trình duyệt trong app có thể không hỗ trợ âm thanh. Vui lòng mở bằng Chrome hoặc Safari.';

    let voicesReadyPromise = null;
    let activeRecognition = null;
    let isListening = false;
    let retryCount = 0;
    const MAX_RETRY = 10; // Retry trong 5 giây (10 * 500ms)

    // Logging helper
    function log(level, ...args) {
        const prefix = `[MsSmileSpeech ${level.toUpperCase()}]`;
        if (level === 'error') console.error(prefix, ...args);
        else if (level === 'warn') console.warn(prefix, ...args);
        else console.log(prefix, ...args);
    }

    function getSpeechSynthesis() {
        return window.speechSynthesis || null;
    }

    function isWebViewOrInAppBrowser() {
        const ua = navigator.userAgent || '';
        return /\bwv\b|; wv\)|FBAN|FBAV|Instagram|Zalo|Line\/|MicroMessenger/i.test(ua);
    }

    function isSpeechSynthesisSupported() {
        return 'speechSynthesis' in window && typeof window.SpeechSynthesisUtterance === 'function';
    }

    function getEnglishVoice(voices) {
        return voices.find((voice) => voice.lang === 'en-US')
            || voices.find((voice) => voice.lang === 'en-GB')
            || voices.find((voice) => /^en\b/i.test(voice.lang || ''))
            || null;
    }

    function loadVoices() {
        if (!isSpeechSynthesisSupported()) {
            log('warn', 'speechSynthesis not supported');
            return Promise.resolve([]);
        }

        const synthesis = getSpeechSynthesis();
        const currentVoices = synthesis.getVoices();
        log('info', `Current voices count: ${currentVoices.length}`);
        
        if (currentVoices.length > 0) {
            return Promise.resolve(currentVoices);
        }

        if (voicesReadyPromise) {
            return voicesReadyPromise;
        }

        voicesReadyPromise = new Promise((resolve) => {
            let settled = false;
            let attempts = 0;
            const maxAttempts = 10; // 5 giây total (10 * 500ms)
            
            const checkVoices = () => {
                if (settled) return;
                const voices = synthesis.getVoices();
                attempts++;
                log('info', `Attempt ${attempts}: voices count = ${voices.length}`);
                
                if (voices.length > 0) {
                    settled = true;
                    resolve(voices);
                } else if (attempts >= maxAttempts) {
                    settled = true;
                    log('warn', 'Max attempts reached, resolving with empty voices');
                    resolve([]);
                } else {
                    setTimeout(checkVoices, 500);
                }
            };

            synthesis.onvoiceschanged = () => {
                log('info', 'onvoiceschanged triggered');
                checkVoices();
            };
            
            // Bắt đầu retry
            setTimeout(checkVoices, 100);
        });

        return voicesReadyPromise;
    }

    function playAudioUrl(audioUrl) {
        return new Promise((resolve, reject) => {
            const audio = new Audio(audioUrl);
            audio.onended = resolve;
            audio.onerror = () => reject(new Error('Không phát được file âm thanh.'));
            audio.play().catch(reject);
        });
    }

    async function speakText(text, options = {}) {
        const cleanText = String(text || '').trim();
        log('info', 'speakText called:', cleanText.substring(0, 50));
        
        if (!cleanText) {
            log('warn', 'Empty text, skipping');
            return;
        }

        // 1. Thử audioUrl trước nếu có
        if (options.audioUrl) {
            log('info', 'Trying audioUrl:', options.audioUrl);
            try {
                await playAudioUrl(options.audioUrl);
                log('info', 'audioUrl played successfully');
                return;
            } catch (error) {
                log('warn', 'Audio URL failed, falling back to speechSynthesis:', error.message);
            }
        }

        // 2. Kiểm tra speechSynthesis support
        if (!isSpeechSynthesisSupported()) {
            log('error', 'speechSynthesis not supported');
            const isWebView = isWebViewOrInAppBrowser();
            log('info', 'isWebView:', isWebView);
            throw new Error(isWebView ? WEBVIEW_MESSAGE : NO_TTS_MESSAGE);
        }

        const synthesis = getSpeechSynthesis();
        
        // 3. Load voices với retry
        let voices = synthesis.getVoices();
        log('info', `Available voices: ${voices.length}`);
        
        if (voices.length === 0) {
            log('info', 'No voices available, loading...');
            voices = await loadVoices();
        }
        
        // 4. Chọn voice
        let voice = getEnglishVoice(voices);
        if (voice) {
            log('info', 'Using voice:', voice.name, voice.lang);
        } else {
            log('warn', 'No English voice found, using default');
            // Không throw error, dùng default voice
            voice = voices[0] || null;
        }
        
        // 5. Cancel trước khi speak
        synthesis.cancel();
        log('info', 'Cancelled previous speech');

        return new Promise((resolve, reject) => {
            const utterance = new SpeechSynthesisUtterance(cleanText);
            if (voice) {
                utterance.voice = voice;
            }
            utterance.lang = voice?.lang || 'en-US';
            utterance.rate = options.rate || 1;
            utterance.pitch = options.pitch || 1;
            utterance.volume = options.volume || 1;
            
            utterance.onstart = () => {
                log('info', 'Speech started');
                if (typeof options.onStart === 'function') options.onStart();
            };
            
            utterance.onend = () => {
                log('info', 'Speech ended');
                if (typeof options.onEnd === 'function') options.onEnd();
                resolve();
            };
            
            utterance.onerror = (event) => {
                log('error', 'Speech error:', event.error);
                if (typeof options.onEnd === 'function') options.onEnd();
                const errorMsg = event.error === 'not-allowed' ? NO_TTS_MESSAGE : 
                                event.error === 'canceled' ? 'Speech canceled' : 
                                (event.error || NO_TTS_MESSAGE);
                reject(new Error(errorMsg));
            };
            
            log('info', 'Calling synthesis.speak()');
            synthesis.speak(utterance);
        });
    }

    function isSpeechRecognitionSupported() {
        return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
    }

    async function requestMicrophonePermission() {
        log('info', 'Requesting mic permission...');
        log('info', 'isSecureContext:', window.isSecureContext);
        log('info', 'protocol:', window.location.protocol);
        
        if (!window.isSecureContext) {
            log('error', 'Not secure context');
            throw createSpeechError('insecure-context');
        }

        if (!navigator.mediaDevices || typeof navigator.mediaDevices.getUserMedia !== 'function') {
            log('error', 'mediaDevices not supported');
            throw createSpeechError('audio-capture');
        }

        try {
            log('info', 'Calling getUserMedia...');
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            log('info', 'getUserMedia success, stopping tracks');
            stream.getTracks().forEach((track) => track.stop());
            log('info', 'Mic permission granted');
            return true;
        } catch (error) {
            log('error', 'getUserMedia failed:', error.name, error.message);
            if (error && (error.name === 'NotAllowedError' || error.name === 'SecurityError')) {
                throw createSpeechError('not-allowed');
            }
            if (error && (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError')) {
                throw createSpeechError('audio-capture');
            }
            throw createSpeechError('permission-denied');
        }
    }

    function createSpeechError(code) {
        const error = new Error(getSpeechRecognitionErrorMessage(code));
        error.code = code;
        return error;
    }

    function getSpeechRecognitionErrorMessage(code) {
        switch (code) {
            case 'permission-denied':
            case 'not-allowed':
                return NEED_MIC_MESSAGE;
            case 'no-speech':
                return 'Không nghe thấy giọng nói. Bạn thử bấm micro và nói lại rõ hơn nhé.';
            case 'audio-capture':
                return 'Không tìm thấy micro. Vui lòng kiểm tra micro rồi thử lại.';
            case 'network':
                return 'Nhận diện giọng nói cần kết nối mạng ổn định. Vui lòng kiểm tra mạng rồi thử lại.';
            case 'insecure-context':
                return NEED_SECURE_CONTEXT_MESSAGE;
            case 'busy':
                return 'Micro đang nghe rồi. Vui lòng chờ kết thúc trước khi bấm lại.';
            case 'unsupported':
                return isWebViewOrInAppBrowser() ? OPEN_BROWSER_MESSAGE : NO_RECOGNITION_MESSAGE;
            default:
                return 'Chưa nhận diện được giọng nói. Bạn thử lại nhé.';
        }
    }

    async function startSpeechRecognition(options = {}) {
        log('info', 'startSpeechRecognition called, lang:', options.lang || 'en-US');
        
        if (!isSpeechRecognitionSupported()) {
            log('error', 'SpeechRecognition not supported');
            throw createSpeechError('unsupported');
        }
        if (isListening) {
            log('warn', 'Already listening, throwing busy error');
            throw createSpeechError('busy');
        }

        await requestMicrophonePermission();

        const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        log('info', 'Creating SpeechRecognition instance');
        const recognition = new Recognition();
        activeRecognition = recognition;
        isListening = true;

        recognition.lang = options.lang || 'en-US';
        recognition.interimResults = false;
        recognition.continuous = false;

        return new Promise((resolve, reject) => {
            let hasResult = false;

            recognition.onstart = () => {
                log('info', 'Recognition started');
                if (typeof options.onStart === 'function') options.onStart();
            };

            recognition.onresult = (event) => {
                log('info', 'Recognition got result');
                hasResult = true;
                const transcript = event.results && event.results[0] && event.results[0][0]
                    ? event.results[0][0].transcript
                    : '';
                log('info', 'Transcript:', transcript);
                resolve(transcript);
            };

            recognition.onerror = (event) => {
                log('error', 'Recognition error:', event.error);
                isListening = false;
                activeRecognition = null;
                reject(createSpeechError(event.error || 'unknown'));
            };

            recognition.onend = () => {
                log('info', 'Recognition ended, hasResult:', hasResult);
                isListening = false;
                activeRecognition = null;
                if (typeof options.onEnd === 'function') options.onEnd();
                if (!hasResult) {
                    resolve('');
                }
            };

            try {
                log('info', 'Calling recognition.start()');
                recognition.start();
            } catch (error) {
                log('error', 'recognition.start() failed:', error);
                isListening = false;
                activeRecognition = null;
                reject(createSpeechError(error && error.name === 'InvalidStateError' ? 'busy' : 'unknown'));
            }
        });
    }

    function stopSpeechRecognition() {
        if (activeRecognition) {
            try {
                activeRecognition.stop();
            } catch (error) {
                console.warn('Stop recognition failed:', error);
            }
        }
        isListening = false;
    }

    function debugSupport() {
        const synthesis = getSpeechSynthesis();
        const voices = synthesis ? synthesis.getVoices() : [];
        const result = {
            protocol: window.location.protocol,
            userAgent: navigator.userAgent,
            isSecureContext: window.isSecureContext,
            speechSynthesisSupported: isSpeechSynthesisSupported(),
            voicesCount: voices.length,
            speechRecognitionSupported: isSpeechRecognitionSupported(),
            mediaDevicesSupported: !!(navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === 'function'),
            isWebViewOrInAppBrowser: isWebViewOrInAppBrowser()
        };
        log('info', 'Debug Support:', result);
        return result;
    }

    window.MsSmileSpeech = {
        NO_TTS_MESSAGE,
        NO_RECOGNITION_MESSAGE,
        OPEN_BROWSER_MESSAGE,
        NEED_SECURE_CONTEXT_MESSAGE,
        WEBVIEW_MESSAGE,
        isWebViewOrInAppBrowser,
        isSpeechSynthesisSupported,
        speakText,
        isSpeechRecognitionSupported,
        requestMicrophonePermission,
        startSpeechRecognition,
        stopSpeechRecognition,
        getSpeechRecognitionErrorMessage,
        debugSupport
    };
    
    // Log thông tin khởi tạo
    log('info', 'MsSmileSpeech initialized');
    log('info', 'Protocol:', window.location.protocol);
    log('info', 'isSecureContext:', window.isSecureContext);
    log('info', 'speechSynthesis supported:', isSpeechSynthesisSupported());
    log('info', 'SpeechRecognition supported:', isSpeechRecognitionSupported());
    
    // Auto warmup voices
    if (isSpeechSynthesisSupported()) {
        loadVoices().catch(err => log('warn', 'Voice warmup failed:', err));
    }
})();
