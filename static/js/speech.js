(function () {
    const NO_TTS_MESSAGE = 'Máy này chưa hỗ trợ giọng đọc. Vui lòng mở bằng Chrome hoặc Edge, hoặc bật Google Text-to-Speech.';
    const NO_RECOGNITION_MESSAGE = 'Trình duyệt này chưa hỗ trợ nhận diện giọng nói. Vui lòng dùng Chrome hoặc Edge trên máy tính/Android.';
    const OPEN_BROWSER_MESSAGE = 'Bạn hãy mở bằng Chrome hoặc Edge để dùng chức năng nghe/nói.';
    const NEED_MIC_MESSAGE = 'Bạn cần cho phép quyền micro để luyện nói.';
    const NEED_SECURE_CONTEXT_MESSAGE = 'Micro chỉ hoạt động trên HTTPS hoặc localhost. Vui lòng mở app bằng Chrome/Edge qua HTTPS hoặc chạy trên localhost.';

    let voicesReadyPromise = null;
    let activeRecognition = null;
    let isListening = false;

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
            return Promise.resolve([]);
        }

        const synthesis = getSpeechSynthesis();
        const currentVoices = synthesis.getVoices();
        if (currentVoices.length > 0) {
            return Promise.resolve(currentVoices);
        }

        if (voicesReadyPromise) {
            return voicesReadyPromise;
        }

        voicesReadyPromise = new Promise((resolve) => {
            let settled = false;
            const finish = () => {
                if (settled) return;
                const voices = synthesis.getVoices();
                if (voices.length === 0) return;
                settled = true;
                resolve(voices);
            };

            synthesis.onvoiceschanged = finish;
            setTimeout(() => {
                if (!settled) {
                    settled = true;
                    resolve(synthesis.getVoices());
                }
            }, 1500);
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
        if (!cleanText) return;

        if (options.audioUrl) {
            try {
                await playAudioUrl(options.audioUrl);
                return;
            } catch (error) {
                console.warn('Audio URL failed, falling back to speechSynthesis:', error);
            }
        }

        if (!isSpeechSynthesisSupported()) {
            throw new Error(isWebViewOrInAppBrowser() ? OPEN_BROWSER_MESSAGE : NO_TTS_MESSAGE);
        }

        const synthesis = getSpeechSynthesis();
        const voices = synthesis.getVoices();
        const voice = getEnglishVoice(voices);
        if (!voice) {
            loadVoices().catch((error) => console.warn('Voice warmup failed:', error));
        }
        synthesis.cancel();

        return new Promise((resolve, reject) => {
            const utterance = new SpeechSynthesisUtterance(cleanText);
            if (voice) {
                utterance.voice = voice;
            }
            utterance.lang = voice?.lang || 'en-US';
            utterance.rate = options.rate || 1;
            utterance.pitch = options.pitch || 1;
            utterance.volume = options.volume || 1;
            utterance.onstart = options.onStart || null;
            utterance.onend = () => {
                if (typeof options.onEnd === 'function') options.onEnd();
                resolve();
            };
            utterance.onerror = (event) => {
                if (typeof options.onEnd === 'function') options.onEnd();
                reject(new Error(event.error === 'not-allowed' ? NO_TTS_MESSAGE : (event.error || NO_TTS_MESSAGE)));
            };
            synthesis.speak(utterance);
        });
    }

    function isSpeechRecognitionSupported() {
        return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
    }

    async function requestMicrophonePermission() {
        if (!window.isSecureContext) {
            throw createSpeechError('insecure-context');
        }

        if (!navigator.mediaDevices || typeof navigator.mediaDevices.getUserMedia !== 'function') {
            throw createSpeechError('audio-capture');
        }

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            stream.getTracks().forEach((track) => track.stop());
            return true;
        } catch (error) {
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
        if (!isSpeechRecognitionSupported()) {
            throw createSpeechError('unsupported');
        }
        if (isListening) {
            throw createSpeechError('busy');
        }

        await requestMicrophonePermission();

        const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new Recognition();
        activeRecognition = recognition;
        isListening = true;

        recognition.lang = options.lang || 'en-US';
        recognition.interimResults = false;
        recognition.continuous = false;

        return new Promise((resolve, reject) => {
            let hasResult = false;

            recognition.onstart = () => {
                if (typeof options.onStart === 'function') options.onStart();
            };

            recognition.onresult = (event) => {
                hasResult = true;
                const transcript = event.results && event.results[0] && event.results[0][0]
                    ? event.results[0][0].transcript
                    : '';
                resolve(transcript);
            };

            recognition.onerror = (event) => {
                reject(createSpeechError(event.error || 'unknown'));
            };

            recognition.onend = () => {
                isListening = false;
                activeRecognition = null;
                if (typeof options.onEnd === 'function') options.onEnd();
                if (!hasResult) {
                    resolve('');
                }
            };

            try {
                recognition.start();
            } catch (error) {
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

    window.MsSmileSpeech = {
        NO_TTS_MESSAGE,
        NO_RECOGNITION_MESSAGE,
        OPEN_BROWSER_MESSAGE,
        NEED_SECURE_CONTEXT_MESSAGE,
        isWebViewOrInAppBrowser,
        isSpeechSynthesisSupported,
        speakText,
        isSpeechRecognitionSupported,
        requestMicrophonePermission,
        startSpeechRecognition,
        stopSpeechRecognition,
        getSpeechRecognitionErrorMessage
    };
})();
