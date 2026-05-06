/**
 * Ms. Smile English - Main JavaScript Application
 * Xử lý tất cả chức năng frontend
 */
const APP_VERSION = "hybrid-roadmap-015";
console.log('[APP_VERSION]', APP_VERSION);

// ==========================================
// Global State
// ==========================================
const state = {
    conversationHistory: [],
    isRecording: false,
    recognition: null,
    synthesis: window.speechSynthesis,
    ttsEnabled: true,
    ttsSpeed: 1.0,
    currentUser: null,
    profile: null,
    userToken: null,
    
    // Freemium
    isGuest: true,
    guestLimits: {
        chat: 0,
        situation: 0,
        roleplay: 0,
        lastReset: null
    },
    currentLesson: null,
    currentPracticeIndex: 0,
    userProfile: null,
    isSpeaking: false,
    
    // Roleplay state
    roleplayRole: null,
    roleplaySituation: null,
    roleplayHistory: [],
    currentAIResponse: null,
    currentAnalysis: null,
    
    // Situation Advisor state
    currentSituation: null,
    currentSituationAdvice: null,
    roadmapCache: null,
    roadmapCacheAt: 0,
    selectedRoadmapLevelId: null,
    currentRoadmapLesson: null,
    currentSpeakingExpected: '',
    currentSpeakingTranscript: '',
    currentUserAudioUrl: null,
    audioCache: new Map(),
    mediaRecorder: null,
    recordedChunks: [],
    
    // User state
    currentUser: null,
    pendingUserId: null  // For profile setup after registration
};

// ==========================================
// DOM Elements
// ==========================================
const elements = {
    // Chat
    chatMessages: document.getElementById('chatMessages'),
    messageInput: document.getElementById('messageInput'),
    sendBtn: document.getElementById('sendBtn'),
    micBtn: document.getElementById('micBtn'),
    recordingIndicator: document.getElementById('recordingIndicator'),
    clearChatBtn: document.getElementById('clearChatBtn'),
    
    // Buttons
    lessonBtn: document.getElementById('lessonBtn'),
    roadmapBtn: document.getElementById('roadmapBtn'),
    statsBtn: document.getElementById('statsBtn'),
    startLessonBtn: document.getElementById('startLessonBtn'),
    profileBtn: document.getElementById('profileBtn'),
    feedbackBtn: document.getElementById('feedbackBtn'),
    plansBtn: document.getElementById('plansBtn'),
    
    // Modals
    lessonModal: document.getElementById('lessonModal'),
    roadmapModal: document.getElementById('roadmapModal'),
    statsModal: document.getElementById('statsModal'),
    speakingModal: document.getElementById('speakingModal'),
    onboardingModal: document.getElementById('onboardingModal'),
    profileModal: document.getElementById('profileModal'),
    feedbackModal: document.getElementById('feedbackModal'),
    planModal: document.getElementById('planModal'),
    
    // Modal content
    lessonLoading: document.getElementById('lessonLoading'),
    lessonContent: document.getElementById('lessonContent'),
    statsContent: document.getElementById('statsContent'),
    
    // Stats
    statLessons: document.getElementById('statLessons'),
    statChats: document.getElementById('statChats'),
    statSpeaking: document.getElementById('statSpeaking'),
    statDays: document.getElementById('statDays'),
    mistakesList: document.getElementById('mistakesList'),
    
    // Speaking
    practiceText: document.getElementById('practiceText'),
    playPracticeBtn: document.getElementById('playPracticeBtn'),
    recordPracticeBtn: document.getElementById('recordPracticeBtn'),
    speakingResult: document.getElementById('speakingResult'),
    
    // Onboarding & Profile
    onboardingForm: document.getElementById('onboardingForm'),
    profileForm: document.getElementById('profileForm'),
    feedbackForm: document.getElementById('feedbackForm'),
    resetProfileBtn: document.getElementById('resetProfileBtn'),
    
    // Auth
    loginBtn: document.getElementById('loginBtn'),
    registerBtn: document.getElementById('registerBtn'),
    logoutBtn: document.getElementById('logoutBtn'),
    loginModal: document.getElementById('loginModal'),
    loginForm: document.getElementById('loginForm'),
    registerModal: document.getElementById('registerModal'),
    registerForm: document.getElementById('registerForm'),
    profileSetupModal: document.getElementById('profileSetupModal'),
    profileSetupForm: document.getElementById('profileSetupForm'),
    switchToRegister: document.getElementById('switchToRegister'),
    dashboardBtn: document.getElementById('dashboardBtn'),
    affiliateBtn: document.getElementById('affiliateBtn'),
    adminBtn: document.getElementById('adminBtn'),
    dashboardModal: document.getElementById('dashboardModal'),
    dashboardContent: document.getElementById('dashboardContent'),
    affiliateModal: document.getElementById('affiliateModal'),
    affiliateCode: document.getElementById('affiliateCode'),
    affiliateLink: document.getElementById('affiliateLink'),
    copyAffiliateLinkBtn: document.getElementById('copyAffiliateLinkBtn'),
    affiliateReferredCount: document.getElementById('affiliateReferredCount'),
    affiliatePaidCount: document.getElementById('affiliatePaidCount'),
    affiliatePending: document.getElementById('affiliatePending'),
    affiliatePaid: document.getElementById('affiliatePaid'),
    
    // Freemium
    userBadge: document.getElementById('userBadge'),
    userBadgeText: document.getElementById('userBadgeText'),
    limitModal: document.getElementById('limitModal'),
    chatLimitDisplay: document.getElementById('chatLimitDisplay'),
    situationLimitDisplay: document.getElementById('situationLimitDisplay'),
    roleplayLimitDisplay: document.getElementById('roleplayLimitDisplay'),
    limitRegisterBtn: document.getElementById('limitRegisterBtn'),
    limitLoginBtn: document.getElementById('limitLoginBtn'),
    
    // TTS & Avatar
    aiAvatar: document.getElementById('aiAvatar'),
    avatarMouth: document.getElementById('avatarMouth'),
    eyeLeft: document.getElementById('eyeLeft'),
    eyeRight: document.getElementById('eyeRight'),
    speechStatus: document.getElementById('speechStatus'),
    ttsControls: document.getElementById('ttsControls'),
    replayTTSBtn: document.getElementById('replayTTSBtn'),
    recordAgainBtn: document.getElementById('recordAgainBtn'),
    ttsVoice: document.getElementById('ttsVoice'),
    voiceSelector: document.getElementById('voiceSelector'),
    
    // Roleplay
    roleplayBtn: document.getElementById('roleplayBtn'),
    roleplayModal: document.getElementById('roleplayModal'),
    roleplaySetup: document.getElementById('roleplaySetup'),
    activeRoleplay: document.getElementById('activeRoleplay'),
    startRoleplayBtn: document.getElementById('startRoleplayBtn'),
    roleplayMessages: document.getElementById('roleplayMessages'),
    roleplayInput: document.getElementById('roleplayInput'),
    roleplaySendBtn: document.getElementById('roleplaySendBtn'),
    roleplayMicBtn: document.getElementById('roleplayMicBtn'),
    roleplayAnalysis: document.getElementById('roleplayAnalysis'),
    listenAIBtn: document.getElementById('listenAIBtn'),
    suggestAnswerBtn: document.getElementById('suggestAnswerBtn'),
    correctMeBtn: document.getElementById('correctMeBtn'),
    sayNaturallyBtn: document.getElementById('sayNaturallyBtn'),
    endRoleplayBtn: document.getElementById('endRoleplayBtn'),
    roleplaySituation: document.getElementById('roleplaySituation'),
    
    // Situation Advisor
    situationBtn: document.getElementById('situationBtn'),
    situationModal: document.getElementById('situationModal'),
    situationInput: document.getElementById('situationInput'),
    analyzeSituationBtn: document.getElementById('analyzeSituationBtn'),
    situationInputSection: document.getElementById('situationInputSection'),
    situationResult: document.getElementById('situationResult'),
    situationAnalysis: document.getElementById('situationAnalysis'),
    simpleSentenceBtn: document.getElementById('simpleSentenceBtn'),
    naturalSentenceBtn: document.getElementById('naturalSentenceBtn'),
    practiceSituationBtn: document.getElementById('practiceSituationBtn'),
    newSituationBtn: document.getElementById('newSituationBtn'),
    situationPracticeSection: document.getElementById('situationPracticeSection'),
    situationPracticeInput: document.getElementById('situationPracticeInput'),
    situationPracticeSendBtn: document.getElementById('situationPracticeSendBtn'),
    situationPracticeMicBtn: document.getElementById('situationPracticeMicBtn'),
    situationPracticeFeedback: document.getElementById('situationPracticeFeedback'),
    practicePromptText: document.getElementById('practicePromptText'),
    
    // Toast
    toast: document.getElementById('toast'),
    toastIcon: document.getElementById('toastIcon'),
    toastMessage: document.getElementById('toastMessage')
};

// ==========================================
// Initialization
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    captureReferralCode();
    setupEventListeners();
    setupHeaderMoreMenu();
    initializeSpeechRecognition();
    initializeTTS();
    
    // Load freemium limits and update badge
    loadGuestLimits();
    updateUserBadge();
    loadInitialData();
    checkOnboarding();
    
    console.log('🌟 Ms. Smile English đã sẵn sàng!');
}

function setupHeaderMoreMenu() {
    const header = document.querySelector('.header-actions');
    if (!header || document.getElementById('moreMenuWrap')) return;
    const movedItems = [
        elements.statsBtn,
        elements.dashboardBtn,
        elements.affiliateBtn,
        elements.profileBtn,
        elements.feedbackBtn
    ].filter(Boolean);
    if (!movedItems.length) return;

    const wrap = document.createElement('div');
    wrap.id = 'moreMenuWrap';
    wrap.className = 'more-menu-wrap';
    wrap.innerHTML = `
        <button id="moreMenuBtn" class="btn btn-more" type="button">
            <i class="fas fa-ellipsis-h"></i> Them
        </button>
        <div id="moreMenuPanel" class="more-menu-panel hidden"></div>
    `;

    header.insertBefore(wrap, elements.plansBtn || elements.userBadge || null);
    const panel = document.getElementById('moreMenuPanel');
    movedItems.forEach(item => panel.appendChild(item));

    document.getElementById('moreMenuBtn').addEventListener('click', (event) => {
        event.stopPropagation();
        panel.classList.toggle('hidden');
    });
    panel.addEventListener('click', () => panel.classList.add('hidden'));
    document.addEventListener('click', () => panel.classList.add('hidden'));
}

function captureReferralCode() {
    const params = new URLSearchParams(window.location.search);
    const ref = params.get('ref');
    if (ref) {
        state.referralCode = ref;
        localStorage.setItem('ms_smile_referral_code', ref);
    } else {
        const storedRef = localStorage.getItem('ms_smile_referral_code');
        if (storedRef) {
            state.referralCode = storedRef;
        }
    }
}

function openAffiliateModal() {
    if (!state.currentUser) {
        showToast('⚠️', 'Vui lòng đăng nhập để sử dụng tính năng giới thiệu.');
        openModal('loginModal');
        return;
    }
    loadAffiliateData();
    openModal('affiliateModal');
}

async function loadAffiliateData() {
    try {
        const response = await fetch(`/api/user/affiliate?user_id=${state.currentUser.id}`);
        const data = await response.json();
        if (!data.success) {
            showToast('❌', data.error || 'Không thể tải dữ liệu affiliate');
            return;
        }
        const affiliate = data.affiliate || {};
        const profile = affiliate.profile || {};
        elements.affiliateCode.value = profile.affiliate_code || '';
        elements.affiliateLink.value = profile.referral_link || '';
        elements.affiliateReferredCount.textContent = (profile.total_referrals || 0).toString();
        elements.affiliatePending.textContent = (profile.pending_commission || 0).toString();
        elements.affiliatePaid.textContent = (profile.paid_commission || 0).toString();
        const paidCount = (affiliate.commissions || []).filter(c => c.status === 'paid').length;
        elements.affiliatePaidCount.textContent = paidCount.toString();
    } catch (error) {
        console.error('Affiliate load error:', error);
        showToast('❌', 'Lỗi tải affiliate');
    }
}

function copyAffiliateLink() {
    if (!elements.affiliateLink || !elements.affiliateLink.value) return;
    navigator.clipboard.writeText(elements.affiliateLink.value)
        .then(() => showToast('✅', 'Đã sao chép link giới thiệu!'))
        .catch((err) => {
            console.error('Copy error:', err);
            showToast('❌', 'Sao chép thất bại');
        });
}

// ==========================================
// Onboarding & Profile Functions
// ==========================================
async function checkOnboarding() {
    try {
        const response = await fetch('/api/profile/onboarded');
        const data = await response.json();
        
        if (!data.onboarded) {
            // Hiển thị onboarding modal
            openModal('onboardingModal');
        } else {
            // Load profile
            await loadUserProfile();
        }
    } catch (error) {
        console.error('Lỗi kiểm tra onboarding:', error);
    }
}

async function loadUserProfile() {
    try {
        const response = await fetch('/api/profile');
        const data = await response.json();
        
        if (data.success) {
            state.userProfile = data.profile;
            console.log('Profile loaded:', state.userProfile);
        }
    } catch (error) {
        console.error('Lỗi load profile:', error);
    }
}

async function saveOnboarding(formData) {
    try {
        const response = await fetch('/api/profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...formData,
                onboarded: true,
                created_at: new Date().toISOString()
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            state.userProfile = data.profile;
            closeModal('onboardingModal');
            showToast('✅', `Chào ${formData.name}! Cô sẽ giúp em học tiếng Anh nhé! 😊`);
            
            // Cập nhật welcome message với tên
            updateWelcomeMessage(formData.name);
            const recommendedLevel = getOnboardingRecommendedLevel(formData);
            openModal('roadmapModal');
            await loadRoadmapLevel(recommendedLevel);
            const firstLesson = recommendedLevel === 'flyer' ? 'flyer_u1_lesson_1' : 'starter_u1_lesson_1';
            setTimeout(() => openRoadmapLesson(firstLesson), 250);
        }
    } catch (error) {
        console.error('Lỗi save onboarding:', error);
        showToast('❌', 'Có lỗi xảy ra. Em thử lại nhé!');
    }
}

function getOnboardingRecommendedLevel(profile) {
    if (profile.goal === 'ielts') return 'ielts_foundation';
    if (profile.level === 'intermediate') return 'flyer';
    return 'starter';
}

async function updateProfile(formData) {
    try {
        const response = await fetch('/api/user/profile', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            state.currentUser = data.user;
            updateUserBadge();
            closeModal('profileModal');
            showToast('✅', 'Đã cập nhật hồ sơ!');
        } else {
            showToast('❌', data.error || 'Cập nhật thất bại');
        }
    } catch (error) {
        console.error('Lỗi update profile:', error);
        showToast('❌', 'Có lỗi xảy ra. Em thử lại nhé!');
    }
}

async function loadFamilyMembers() {
    const section = document.getElementById('familySection');
    const list = document.getElementById('familyMembersList');
    if (!section || !list || !state.currentUser?.id) return;
    const isFamily = (state.currentUser.plan_name || '').toLowerCase().includes('family') && state.currentUser.status === 'active';
    section.classList.toggle('hidden', !isFamily);
    if (!isFamily) return;
    list.innerHTML = '<div class="loading-state small">Dang tai thanh vien...</div>';
    try {
        const response = await fetch(`/api/family/members?user_id=${state.currentUser.id}`);
        const data = await response.json();
        if (!data.success) throw new Error(data.error || 'Family error');
        list.innerHTML = `
            <div class="family-capacity">${data.used_slots || 0}/${data.member_slots || 4} thanh vien da dung</div>
            ${(data.members || []).map(member => `
                <div class="family-member-row">
                    <div>
                        <strong>${escapeHtml(member.name || 'Thanh vien')}</strong>
                        <span>${escapeHtml(member.email || member.phone || '')}</span>
                        <small>${escapeHtml(member.status || '')}</small>
                    </div>
                    <button type="button" class="btn btn-secondary" onclick="removeFamilyMember(${member.id})">Xoa</button>
                </div>
            `).join('') || '<p class="empty-text">Chua co thanh vien nao.</p>'}
        `;
    } catch (error) {
        console.error('Family load error:', error);
        list.innerHTML = '<p class="empty-text">Khong tai duoc danh sach Family.</p>';
    }
}

async function inviteFamilyMember() {
    if (!state.currentUser?.id) return;
    const payload = {
        user_id: state.currentUser.id,
        name: document.getElementById('familyMemberName')?.value || '',
        email: document.getElementById('familyMemberEmail')?.value || '',
        phone: document.getElementById('familyMemberPhone')?.value || ''
    };
    if (!payload.email && !payload.phone) {
        showToast('⚠️', 'Nhap email hoac so dien thoai thanh vien');
        return;
    }
    const response = await fetch('/api/family/members', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (data.success) {
        ['familyMemberName', 'familyMemberEmail', 'familyMemberPhone'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = '';
        });
        showToast('✅', data.message || 'Da them thanh vien');
        loadFamilyMembers();
    } else {
        showToast('❌', data.error || 'Khong them duoc thanh vien');
    }
}

async function removeFamilyMember(memberId) {
    if (!state.currentUser?.id) return;
    const response = await fetch(`/api/family/members/${memberId}?user_id=${state.currentUser.id}`, { method: 'DELETE' });
    const data = await response.json();
    if (data.success) {
        showToast('✅', data.message || 'Da xoa thanh vien');
        loadFamilyMembers();
    } else {
        showToast('❌', data.error || 'Khong xoa duoc thanh vien');
    }
}

async function resetProfile() {
    try {
        const response = await fetch('/api/profile/reset', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            showToast('🔄', 'Đã reset hồ sơ!');
            openModal('onboardingModal');
        }
    } catch (error) {
        console.error('Lỗi reset profile:', error);
    }
}

async function handleFeedbackSubmit(e) {
    e.preventDefault();
    
    const category = document.getElementById('feedbackCategory').value;
    const content = document.getElementById('feedbackContent').value;
    const rating = document.querySelector('input[name="rating"]:checked')?.value || 0;
    
    if (!category || !content) {
        showToast('❌', 'Vui lòng điền đầy đủ thông tin');
        return;
    }
    
    try {
        const response = await fetch('/api/user/submit-feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category, content, rating: parseInt(rating) })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Reset form
            document.getElementById('feedbackForm').reset();
            closeModal('feedbackModal');
            showToast('✅', 'Cảm ơn phản hồi của em! Chúng mình sẽ xem xét nhé.');
        } else {
            showToast('❌', data.error || 'Gửi phản hồi thất bại');
        }
    } catch (error) {
        console.error('Feedback submit error:', error);
        showToast('❌', 'Có lỗi xảy ra, thử lại nhé!');
    }
}

function updateWelcomeMessage(name) {
    const welcomeMsg = document.querySelector('.message-ai .message-content');
    if (welcomeMsg && name) {
        const p = welcomeMsg.querySelector('p');
        if (p) {
            p.textContent = `Xin chào ${name}! 🌟`;
        }
    }
}

function populateProfileForm() {
    if (!state.currentUser) return;
    
    const u = state.currentUser;
    document.getElementById('profileName').value = u.name || '';
    document.getElementById('profileEmail').value = u.email || '';
    document.getElementById('profilePhone').value = u.phone || '';
    document.getElementById('profileAge').value = u.age || '';
    document.getElementById('profileJob').value = u.job || '';
    document.getElementById('profileUsage').value = u.english_usage || '';
    document.getElementById('profileGoal').value = u.goal || '';
    document.getElementById('profileLevel').value = u.english_level || 'beginner';
    state.selectedRoadmapLevelId = u.selected_roadmap_level || state.selectedRoadmapLevelId;
    
    // Set radio button for meet_foreigners
    const meetForeignersRadios = document.querySelectorAll('input[name="profileMeetForeigners"]');
    meetForeignersRadios.forEach(radio => {
        radio.checked = (radio.value === 'true') === u.meet_foreigners;
    });
    
    // Load current plan info
    loadCurrentPlanInfo();
    loadFamilyMembers();
}

function setupEventListeners() {
    // Chat
    elements.sendBtn.addEventListener('click', sendMessage);
    elements.messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    elements.micBtn.addEventListener('click', toggleRecording);
    elements.clearChatBtn.addEventListener('click', clearChat);
    
    // Buttons
    elements.lessonBtn.addEventListener('click', () => openModal('lessonModal'));
    if (elements.roadmapBtn) {
        elements.roadmapBtn.addEventListener('click', () => {
            openModal('roadmapModal');
            openSavedRoadmap();
        });
    }
    elements.statsBtn.addEventListener('click', () => {
        loadStats();
        openModal('statsModal');
    });
    elements.startLessonBtn.addEventListener('click', () => {
        openModal('roadmapModal');
        openSavedRoadmap();
    });
    if (elements.plansBtn) {
        elements.plansBtn.addEventListener('click', () => {
            loadPlanOptions();
            openModal('planModal');
        });
    }
    const placementBtn = document.getElementById('placementTestBtn');
    if (placementBtn) {
        placementBtn.addEventListener('click', startPlacementTest);
    }
    const continueRoadmapBtn = document.getElementById('continueRoadmapBtn');
    if (continueRoadmapBtn) {
        continueRoadmapBtn.addEventListener('click', continueRoadmapLesson);
    }
    
    // Close modals
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal(modal.id);
        });
    });
    
    // Speaking practice
    elements.playPracticeBtn.addEventListener('click', () => {
        const text = elements.practiceText.textContent;
        console.log('[PracticeAudio] loa xanh clicked');
        console.log('[PracticeAudio] text:', text);
        speakText(text);
        console.log('[PracticeAudio] speakText called');
    });
    elements.recordPracticeBtn.addEventListener('click', togglePracticeRecording);
    
    // Profile button
    elements.profileBtn.addEventListener('click', () => {
        populateProfileForm();
        openModal('profileModal');
    });
    
    // Feedback button
    elements.feedbackBtn.addEventListener('click', () => {
        openModal('feedbackModal');
    });
    
    // Freemium limit modal buttons
    if (elements.limitRegisterBtn) {
        elements.limitRegisterBtn.addEventListener('click', () => {
            closeModal('limitModal');
            openModal('registerModal');
        });
    }
    
    if (elements.limitLoginBtn) {
        elements.limitLoginBtn.addEventListener('click', () => {
            closeModal('limitModal');
            openModal('loginModal');
        });
    }
    
    // Onboarding form
    if (elements.onboardingForm) {
        elements.onboardingForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = {
                name: document.getElementById('userName').value,
                age: document.getElementById('userAge').value,
                level: document.getElementById('userLevel').value,
                goal: document.getElementById('userGoal').value,
                job: document.getElementById('userJob').value,
                field: document.getElementById('userField').value,
                daily_time: document.getElementById('userTime').value
            };
            saveOnboarding(formData);
        });
    }
    
    // Profile form
    if (elements.profileForm) {
        elements.profileForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const form = e.currentTarget;
            const formData = {
                user_id: state.currentUser.id,
                profile: {
                    name: form.querySelector('#profileName').value,
                    age: form.querySelector('#profileAge').value,
                    job: form.querySelector('#profileJob').value,
                    meet_foreigners: form.querySelector('input[name="profileMeetForeigners"]:checked')?.value === 'true',
                    english_usage: form.querySelector('#profileUsage').value,
                    goal: form.querySelector('#profileGoal').value,
                    level: form.querySelector('#profileLevel').value,
                    selected_roadmap_level: state.selectedRoadmapLevelId || state.currentUser?.selected_roadmap_level || ''
                }
            };
            updateProfile(formData);
        });
    }
    
    // Reset profile
    if (elements.resetProfileBtn) {
        elements.resetProfileBtn.addEventListener('click', () => {
            if (confirm('Em có chắc muốn học lại từ đầu không?')) {
                resetProfile();
            }
        });
    }
    
    // Plan upgrade button
    const upgradePlanBtn = document.getElementById('upgradePlanBtn');
    if (upgradePlanBtn) {
        upgradePlanBtn.addEventListener('click', () => {
            loadPlanOptions();
            openModal('planModal');
        });
    }
    
    // Feedback form
    if (elements.feedbackForm) {
        elements.feedbackForm.addEventListener('submit', handleFeedbackSubmit);
    }
    
    // TTS speed
    if (elements.ttsSpeed) {
        elements.ttsSpeed.addEventListener('change', (e) => {
            state.ttsSpeed = parseFloat(e.target.value);
            console.log('TTS speed:', state.ttsSpeed);
        });
    }
    
    // TTS Voice selector
    if (elements.ttsVoice) {
        elements.ttsVoice.addEventListener('change', (e) => {
            state.ttsVoice = e.target.value;
            console.log('TTS voice:', state.ttsVoice);
        });
    }
    
    // Replay TTS button
    if (elements.replayTTSBtn) {
        elements.replayTTSBtn.addEventListener('click', () => {
            if (state.lastAIResponse) {
                speakText(state.lastAIResponse);
            }
        });
    }

    // Daily lesson audio buttons (event delegation)
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.daily-audio-btn');
        
        if (!btn) {
            return;
        }

        e.preventDefault();
        e.stopPropagation();

        const text = btn.dataset.speakText;
        const section = btn.dataset.section;
        console.log('[DailyLessonAudio] clicked', { section, text });

        if (!text || !text.trim()) {
            console.warn('[DailyLessonAudio] empty text, skipping');
            return;
        }

        playDailyLessonAudio(text, btn);
    });
    
    // Record again button (focus input and start voice recognition)
    if (elements.recordAgainBtn) {
        elements.recordAgainBtn.addEventListener('click', () => {
            elements.messageInput.focus();
            startVoiceRecording();
        });
    }
    
    // Roleplay button
    if (elements.roleplayBtn) {
        elements.roleplayBtn.addEventListener('click', () => {
            openModal('roleplayModal');
            resetRoleplayUI();
        });
    }
    
    // Situation Advisor button
    if (elements.situationBtn) {
        elements.situationBtn.addEventListener('click', () => {
            openModal('situationModal');
            resetSituationUI();
        });
    }
    
    // Example chips for situation
    document.querySelectorAll('.example-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            if (elements.situationInput) {
                elements.situationInput.value = chip.dataset.example;
            }
        });
    });
    
    // Analyze situation
    if (elements.analyzeSituationBtn) {
        elements.analyzeSituationBtn.addEventListener('click', analyzeSituation);
    }
    
    if (elements.situationInput) {
        elements.situationInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                analyzeSituation();
            }
        });
    }
    
    // Situation control buttons
    if (elements.simpleSentenceBtn) {
        elements.simpleSentenceBtn.addEventListener('click', () => {
            speakText(state.currentSituationAdvice?.simple_en || '');
        });
    }
    
    if (elements.naturalSentenceBtn) {
        elements.naturalSentenceBtn.addEventListener('click', () => {
            speakText(state.currentSituationAdvice?.natural_en || '');
        });
    }
    
    if (elements.practiceSituationBtn) {
        elements.practiceSituationBtn.addEventListener('click', startSituationPractice);
    }
    
    if (elements.newSituationBtn) {
        elements.newSituationBtn.addEventListener('click', resetSituationUI);
    }
    
    // Situation practice
    if (elements.situationPracticeSendBtn) {
        elements.situationPracticeSendBtn.addEventListener('click', submitSituationPractice);
    }
    
    if (elements.situationPracticeInput) {
        elements.situationPracticeInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') submitSituationPractice();
        });
    }
    
    if (elements.situationPracticeMicBtn) {
        elements.situationPracticeMicBtn.addEventListener('click', toggleSituationPracticeRecording);
    }
    
    // Auth buttons
    if (elements.loginBtn) {
        elements.loginBtn.addEventListener('click', () => openModal('loginModal'));
    }
    
    if (elements.registerBtn) {
        elements.registerBtn.addEventListener('click', () => openModal('registerModal'));
    }
    
    if (elements.logoutBtn) {
        elements.logoutBtn.addEventListener('click', logout);
    }
    
    if (elements.dashboardBtn) {
        elements.dashboardBtn.addEventListener('click', showDashboard);
    }
    if (elements.affiliateBtn) {
        elements.affiliateBtn.addEventListener('click', openAffiliateModal);
    }
    if (elements.adminBtn) {
        elements.adminBtn.addEventListener('click', () => {
            const userId = state.currentUser?.id;
            if (userId) {
                window.location.href = `/admin?admin_id=${userId}`;
            } else {
                showToast('⚠️', 'Chỉ admin mới có thể truy cập trang này.');
            }
        });
    }
    
    if (elements.copyAffiliateLinkBtn) {
        elements.copyAffiliateLinkBtn.addEventListener('click', copyAffiliateLink);
    }
    
    // Auth forms
    if (elements.loginForm) {
        elements.loginForm.addEventListener('submit', handleLogin);
    }
    
    if (elements.registerForm) {
        elements.registerForm.addEventListener('submit', handleRegister);
    }
    
    if (elements.profileSetupForm) {
        elements.profileSetupForm.addEventListener('submit', handleProfileSetup);
    }
    
    // Switch between login/register
    if (elements.switchToRegister) {
        elements.switchToRegister.addEventListener('click', (e) => {
            e.preventDefault();
            closeModal('loginModal');
            openModal('registerModal');
        });
    }
    
    // Role selection
    document.querySelectorAll('.role-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.role-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            state.roleplayRole = btn.dataset.role;
        });
    });
    
    // Start roleplay
    if (elements.startRoleplayBtn) {
        elements.startRoleplayBtn.addEventListener('click', startRoleplay);
    }
    
    // Roleplay chat
    if (elements.roleplaySendBtn) {
        elements.roleplaySendBtn.addEventListener('click', sendRoleplayMessage);
    }
    
    if (elements.roleplayInput) {
        elements.roleplayInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendRoleplayMessage();
        });
    }
    
    // Roleplay mic
    if (elements.roleplayMicBtn) {
        elements.roleplayMicBtn.addEventListener('click', toggleRoleplayRecording);
    }
    
    // Roleplay control buttons
    if (elements.listenAIBtn) {
        elements.listenAIBtn.addEventListener('click', () => {
            if (state.currentAIResponse) {
                speakText(state.currentAIResponse);
            }
        });
    }
    
    if (elements.correctMeBtn) {
        elements.correctMeBtn.addEventListener('click', showCorrection);
    }
    
    if (elements.sayNaturallyBtn) {
        elements.sayNaturallyBtn.addEventListener('click', showNaturalSuggestion);
    }
    
    if (elements.suggestAnswerBtn) {
        elements.suggestAnswerBtn.addEventListener('click', showAnswerSuggestion);
    }
    
    if (elements.endRoleplayBtn) {
        elements.endRoleplayBtn.addEventListener('click', endRoleplay);
    }
}

function initializeSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        state.recognition = new SpeechRecognition();
        state.recognition.continuous = false;
        state.recognition.interimResults = false;
        state.recognition.lang = 'en-US'; // Mặc định tiếng Anh
        
        state.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            elements.messageInput.value = transcript;
            stopRecording();
            
            // Tự động gửi nếu đang trong chế độ practice
            if (state.isPracticeMode) {
                evaluatePracticeSpeech(transcript);
            }
        };
        
        state.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            stopRecording();
            showToast('❌', 'Không nhận diện được giọng nói. Em thử lại nhé!');
        };
        
        state.recognition.onend = () => {
            stopRecording();
        };
    } else {
        elements.micBtn.style.display = 'none';
        console.log('Browser không hỗ trợ Speech Recognition');
    }
}

// ==========================================
// Chat Functions
// ==========================================
async function sendMessage() {
    const message = elements.messageInput.value.trim();
    if (!message) return;
    
    // Kiểm tra freemium limit cho guest
    if (state.isGuest) {
        const check = checkGuestLimit('chat');
        if (!check.allowed) {
            showLimitModal();
            return;
        }
        incrementGuestLimit('chat');
    }
    
    // Thêm tin nhắn người dùng vào chat
    addMessage(message, 'user');
    elements.messageInput.value = '';
    
    // Hiển thị typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                history: state.conversationHistory
            })
        });
        
        const data = await response.json();
        
        // Xóa typing indicator
        hideTypingIndicator();
        
        if (data.success) {
            // Lấy reply từ data.reply (ưu tiên) hoặc data.response (fallback)
            let botReply = data.reply || data.response || data.message || data.text || 'Không có phản hồi';
            
            // Kiểm tra format song ngữ
            const hasEnglish = botReply.includes('English:') || botReply.includes('🇺🇸');
            const hasVietnamese = botReply.includes('Tiếng Việt:') || botReply.includes('🇻🇳');
            const hasExplanation = botReply.includes('Giải thích:') || botReply.includes('📘');
            
            // Nếu không đúng format, tự bọc lại
            if (!hasEnglish || !hasVietnamese || !hasExplanation) {
                console.log('[CHAT] Format không đúng, tự bọc lại:', botReply);
                botReply = `US English:\n${botReply}\n\nVN Tiếng Việt:\n[Cần dịch tiếng Việt]\n\n📘 Giải thích:\nPhản hồi chưa đúng format song ngữ. Cần kiểm tra AI response.`;
            }
            
            addMessage(botReply, 'ai');
            
            // Cập nhật conversation history
            state.conversationHistory.push(
                { role: 'user', content: message },
                { role: 'assistant', content: botReply }
            );
            
            // Giới hạn history để tránh quá dài
            if (state.conversationHistory.length > 20) {
                state.conversationHistory = state.conversationHistory.slice(-20);
            }
        } else {
            addMessage('❌ Xin lỗi em, cô gặp lỗi rồi. Em thử lại sau nhé!', 'ai');
        }
    } catch (error) {
        hideTypingIndicator();
        addMessage('❌ Không kết nối được với cô. Em kiểm tra mạng nhé!', 'ai');
        console.error('Chat error:', error);
    }
}

function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    
    const avatar = type === 'ai' ? '👩‍🏫' : '🙂';
    const formattedContent = formatMessage(content);
    
    // For AI messages, extract English text for TTS
    let englishText = '';
    if (type === 'ai') {
        // Extract English sentences (basic extraction)
        const englishMatches = content.match(/[A-Za-z][A-Za-z0-9\s',.!?-]{5,}/g);
        if (englishMatches) {
            englishText = englishMatches.join('. ');
        }
    }
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            ${formattedContent}
            ${type === 'ai' && englishText ? `<button class="speak-btn" onclick="speakText('${englishText.replace(/'/g, "\\'")}')" title="Nghe cô đọc">🔊</button>` : ''}
        </div>
    `;
    
    elements.chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function formatMessage(content) {
    // Chuyển đổi markdown đơn giản sang HTML
    return content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>')
        .replace(/- (.*?)<br>/g, '• $1<br>');
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message message-ai typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">👩‍🏫</div>
        <div class="message-content">
            <span class="typing-dots">
                <span></span><span></span><span></span>
            </span>
        </div>
    `;
    typingDiv.id = 'typingIndicator';
    elements.chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

function scrollToBottom() {
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function clearChat() {
    elements.chatMessages.innerHTML = `
        <div class="message message-ai">
            <div class="message-avatar">👩‍🏫</div>
            <div class="message-content">
                <p>Cuộc trò chuyện đã được xóa. Em muốn học gì nào? 😊</p>
            </div>
        </div>
    `;
    state.conversationHistory = [];
}

// ==========================================
// Speech Functions
// ==========================================
function toggleRecording() {
    if (!state.recognition) {
        showToast('❌', 'Trình duyệt của em không hỗ trợ nhận diện giọng nói.');
        return;
    }
    
    if (state.isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
}

function startRecording() {
    state.isRecording = true;
    elements.micBtn.classList.add('recording');
    elements.recordingIndicator.classList.remove('hidden');
    
    try {
        state.recognition.start();
    } catch (error) {
        console.error('Recording error:', error);
        stopRecording();
    }
}

function stopRecording() {
    state.isRecording = false;
    elements.micBtn.classList.remove('recording');
    elements.recordingIndicator.classList.add('hidden');
    
    try {
        state.recognition.stop();
    } catch (error) {
        // Ignore stop errors
    }
}

// ==========================================
// Lesson Functions
// ==========================================
async function loadLesson() {
    elements.lessonLoading.classList.remove('hidden');
    elements.lessonContent.classList.add('hidden');
    
    try {
        const response = await fetch('/api/lesson', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                level: state.currentUser?.english_level || 'beginner',
                roadmap_level: state.selectedRoadmapLevelId || null,
                user_id: state.currentUser?.id || null
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.lesson) {
            state.currentLesson = data.lesson;
            renderLesson(data.lesson);
            elements.lessonLoading.classList.add('hidden');
            elements.lessonContent.classList.remove('hidden');
        } else {
            throw new Error('Invalid lesson data');
        }
    } catch (error) {
        console.error('Lesson error:', error);
        elements.lessonLoading.innerHTML = `
            <p>❌ Cô gặp lỗi khi tạo bài học. Em thử lại sau nhé!</p>
            <button onclick="loadLesson()" class="btn btn-lesson" style="margin-top: 15px;">
                <i class="fas fa-redo"></i> Thử lại
            </button>
        `;
    }
}

function renderLesson(lesson) {
    console.log('[DailyLessonAudit] renderLesson called with lesson:', lesson);
    let html = lesson.title ? `
        <div class="lesson-section lesson-title-section">
            <h3>${escapeHtml(lesson.title)}</h3>
            ${lesson.topic ? `<p>${escapeHtml(lesson.topic)}</p>` : ''}
        </div>
    ` : '';
    
    // Vocabulary Section
    if (lesson.vocabulary && lesson.vocabulary.length > 0) {
        html += `
            <div class="lesson-section">
                <h3>📚 Từ vựng hôm nay (${lesson.vocabulary.length} từ)</h3>
                <div class="vocab-grid">
        `;
        
        lesson.vocabulary.forEach(item => {
            html += `
                <div class="vocab-card">
                    <div class="vocab-word">
                        ${item.word}
                        <button type="button" class="speak-btn daily-audio-btn" data-speak-text="${escapeAttr(item.word)}" data-section="vocabulary">
                            <i class="fas fa-volume-up"></i>
                        </button>
                    </div>
                    <div class="vocab-ipa">${item.ipa || ''}</div>
                    <div class="vocab-meaning">${item.meaning}</div>
                    <div class="vocab-example">${item.example || ''}</div>
                </div>
            `;
        });
        
        html += '</div></div>';
    }
    
    // Sentences Section
    if (lesson.sentences && lesson.sentences.length > 0) {
        html += `
            <div class="lesson-section">
                <h3>📝 Mẫu câu thông dụng</h3>
        `;
        
        lesson.sentences.forEach(item => {
            html += `
                <div class="sentence-card">
                    <div class="sentence-en">
                        ${item.english}
                        <button type="button" class="speak-btn daily-audio-btn" data-speak-text="${escapeAttr(item.english)}" data-section="sentence">
                            <i class="fas fa-volume-up"></i>
                        </button>
                    </div>
                    <div class="sentence-vn">${item.vietnamese}</div>
                    <div class="sentence-situation">💡 ${item.situation}</div>
                </div>
            `;
        });
        
        html += '</div>';
    }
    
    // Dialogue Section
    if (lesson.dialogue && lesson.dialogue.length > 0) {
        html += `
            <div class="lesson-section">
                <h3>🎭 Hội thoại</h3>
                <div class="dialogue-container">
        `;
        
        lesson.dialogue.forEach(line => {
            html += `
                <div class="dialogue-line">
                    <div class="speaker">${line.speaker}</div>
                    <div class="dialogue-content">
                        <div class="dialogue-en">
                            ${line.text}
                            <button type="button" class="speak-btn daily-audio-btn" data-speak-text="${escapeAttr(line.text)}" data-section="dialogue">
                                <i class="fas fa-volume-up"></i>
                            </button>
                        </div>
                        <div class="dialogue-vn">${line.translation}</div>
                    </div>
                </div>
            `;
        });
        
        html += '</div></div>';
    }
    
    // Practice Section
    if (lesson.practice && lesson.practice.length > 0) {
        html += `
            <div class="lesson-section">
                <h3>🎯 Luyện nói (${lesson.practice.length} câu)</h3>
                <ul class="practice-list">
        `;
        
        lesson.practice.forEach((sentence, index) => {
            html += `
                <li class="practice-item">
                    <span class="practice-text">${sentence}</span>
                    <div class="practice-actions">
                        <button type="button" class="btn btn-audio daily-audio-btn" data-speak-text="${escapeAttr(sentence)}" data-section="practice">
                            <i class="fas fa-volume-up"></i>
                        </button>
                        <button class="btn btn-record" onclick="openSpeakingPractice(${index})" style="padding: 8px 15px; font-size: 0.9rem;">
                            <i class="fas fa-microphone"></i> Nói
                        </button>
                    </div>
                </li>
            `;
        });
        
        html += '</ul></div>';
    }
    
    // Exercise Section
    if (lesson.exercise) {
        const ex = lesson.exercise;
        html += `
            <div class="lesson-section">
                <h3>✏️ Bài tập nhỏ</h3>
                <div class="exercise-container">
                    <div class="exercise-question">${ex.question}</div>
                    <div class="exercise-options">
        `;
        
        if (ex.options && ex.options.length > 0) {
            ex.options.forEach(opt => {
                html += `
                    <div class="exercise-option" onclick="checkAnswer(this, '${opt}', '${ex.correct}')">
                        ${opt}
                    </div>
                `;
            });
        }
        
        html += '</div></div></div>';
    }
    
    // Add completion button
    html += `
        <div style="text-align: center; margin-top: 30px;">
            <button class="action-btn" onclick="completeLesson()" style="max-width: 300px; margin: 0 auto;">
                <i class="fas fa-check-circle"></i>
                <span>Hoàn thành bài học!</span>
            </button>
        </div>
    `;
    
    elements.lessonContent.innerHTML = html;
    
    // Audit rendered DOM
    setTimeout(() => {
        console.log('[DailyLessonAudit] DOM audit starting...');
        
        const inlineButtons = elements.lessonContent.querySelectorAll('[onclick]');
        console.warn('[DailyLessonAudit] inline onclick count:', inlineButtons.length);
        if (inlineButtons.length > 0) {
            inlineButtons.forEach((btn, idx) => {
                console.warn(`  [${idx}] ${btn.tagName} onclick="${btn.getAttribute('onclick')?.substring(0, 80)}..."`);
            });
        }
        
        const dailyButtons = elements.lessonContent.querySelectorAll('.daily-audio-btn');
        console.log('[DailyLessonAudit] daily-audio-btn count:', dailyButtons.length);
        if (dailyButtons.length > 0) {
            dailyButtons.forEach((btn, idx) => {
                console.log(`  [${idx}] text="${btn.dataset.speakText?.substring(0, 40)}..." section="${btn.dataset.section}"`);
            });
        }
        
        const speakBtns = elements.lessonContent.querySelectorAll('.speak-btn');
        console.log('[DailyLessonAudit] speak-btn total count:', speakBtns.length);
    }, 100);
}

function checkAnswer(element, selected, correct) {
    const allOptions = element.parentElement.querySelectorAll('.exercise-option');
    
    allOptions.forEach(opt => {
        opt.style.pointerEvents = 'none';
        if (opt.textContent.trim() === correct) {
            opt.classList.add('correct');
        }
    });
    
    if (selected !== correct) {
        element.classList.add('wrong');
        showToast('❌', 'Chưa đúng rồi em! Đáp án đúng là: ' + correct);
    } else {
        showToast('✅', 'Chính xác! Giỏi lắm em! 🎉');
    }
}

function completeLesson() {
    closeModal('lessonModal');
    showToast('🎉', 'Chúc mừng em đã hoàn thành bài học! Cô tự hào về em!');
}

// ==========================================
// Hybrid Roadmap Functions
// ==========================================
async function loadRoadmapLevels() {
    const container = document.getElementById('roadmapLevels');
    const detail = document.getElementById('roadmapDetail');
    if (!container) return;
    container.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>Dang tai lo trinh...</p></div>';
    if (detail) detail.classList.add('hidden');
    try {
        const userParam = state.currentUser?.id ? `?user_id=${state.currentUser.id}` : '';
        const response = await fetch(`/api/roadmap/levels${userParam}`);
        const data = await response.json();
        if (!data.success) throw new Error(data.error || 'Roadmap error');
        container.innerHTML = data.levels.map(level => `
            <div class="roadmap-level-card">
                <div class="roadmap-level-main">
                    <h3>${escapeHtml(level.title)}</h3>
                    <p>${escapeHtml(level.description)}</p>
                    <div class="roadmap-meta">${escapeHtml(level.target)} · ${level.unitCount} units · ${level.lessonCount} lessons</div>
                    <div class="roadmap-progress"><span style="width:${level.progressPercent}%"></span></div>
                    <div class="roadmap-percent">${level.progressPercent}% hoan thanh</div>
                </div>
                <button class="btn btn-primary" onclick="loadRoadmapLevel('${level.id}')">Hoc tu dau</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Roadmap load error:', error);
        container.innerHTML = '<p>Khong tai duoc lo trinh hoc.</p>';
    }
}

async function loadRoadmapLevel(levelId) {
    const detail = document.getElementById('roadmapDetail');
    if (!detail) return;
    detail.classList.remove('hidden');
    detail.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>Dang tai bai hoc...</p></div>';
    const userParam = state.currentUser?.id ? `?user_id=${state.currentUser.id}` : '';
    const response = await fetch(`/api/roadmap/levels/${levelId}${userParam}`);
    const data = await response.json();
    if (!data.success) {
        detail.innerHTML = '<p>Khong tim thay level.</p>';
        return;
    }
    const level = data.level;
    detail.innerHTML = `
        <div class="roadmap-detail-header">
            <h3>${escapeHtml(level.title)}</h3>
            <p>${escapeHtml(level.description)}</p>
        </div>
        ${level.units.map(unit => `
            <div class="roadmap-unit">
                <h4>${escapeHtml(unit.title)}</h4>
                <p>${escapeHtml(unit.description)}</p>
                <div class="roadmap-lessons">
                    ${unit.lessons.map(lesson => `
                        <button class="roadmap-lesson ${lesson.status === 'completed' ? 'completed' : ''}" onclick="openRoadmapLesson('${lesson.id}')">
                            <span>${escapeHtml(lesson.title)}</span>
                            <small>${lesson.type}${lesson.isAiEnabled ? ' · AI optional' : ''}</small>
                        </button>
                    `).join('')}
                </div>
            </div>
        `).join('')}
    `;
}

async function openRoadmapLesson(lessonId) {
    const response = await fetch(`/api/roadmap/lessons/${lessonId}`);
    const data = await response.json();
    if (!data.success) return;
    const lesson = data.lesson;
    const detail = document.getElementById('roadmapDetail');
    detail.innerHTML = `
        <div class="roadmap-lesson-view">
            <button class="btn btn-secondary" onclick="loadRoadmapLevel('${lesson.levelId}')">Quay lai unit</button>
            <h3>${escapeHtml(lesson.title)}</h3>
            <div class="roadmap-content-block">${renderRoadmapContent(lesson)}</div>
            <div class="roadmap-actions">
                ${lesson.isAiEnabled ? `<button class="btn btn-stats" onclick="logRoadmapAiUse('${lesson.aiFeatureType}', '${lesson.id}')">AI giai thich giup toi</button>` : ''}
                <button class="btn btn-primary" onclick="completeRoadmapLesson('${lesson.id}', '${lesson.levelId}')">Hoan thanh bai</button>
            </div>
        </div>
    `;
}

function renderRoadmapContent(lesson) {
    const content = lesson.content || {};
    if (lesson.type === 'vocabulary') {
        return `<div class="roadmap-vocab">${(content.words || []).map(w => `<div><strong>${escapeHtml(w.word)}</strong>: ${escapeHtml(w.meaning)}<br><small>${escapeHtml(w.example)}</small></div>`).join('')}</div>`;
    }
    if (lesson.type === 'grammar') {
        return `<ul>${(content.rules || []).map(rule => `<li>${escapeHtml(rule)}</li>`).join('')}</ul><div>${(content.examples || []).map(ex => `<p>${escapeHtml(ex)}</p>`).join('')}</div>`;
    }
    if (lesson.type === 'quiz') {
        return (content.questions || []).map(q => `<div class="roadmap-quiz"><strong>${escapeHtml(q.question)}</strong><div>${(q.options || []).map(o => `<button class="btn btn-secondary" onclick="this.closest('.roadmap-quiz').querySelector('em').textContent='Dap an: ${escapeHtml(q.answer)}'">${escapeHtml(o)}</button>`).join(' ')}</div><em></em></div>`).join('');
    }
    if (lesson.type === 'listening') {
        return (content.dialogue || []).map(line => `<p><strong>${escapeHtml(line.speaker)}:</strong> ${escapeHtml(line.text)}</p>`).join('');
    }
    return `<pre>${escapeHtml(JSON.stringify(content, null, 2))}</pre>`;
}

async function completeRoadmapLesson(lessonId, levelId) {
    if (state.currentUser) {
        await fetch('/api/roadmap/progress', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: state.currentUser.id, lesson_id: lessonId, status: 'completed' })
        });
    }
    showToast('✅', 'Da luu tien do bai hoc');
    loadRoadmapLevel(levelId);
}

function renderRoadmapSkeleton() {
    return Array.from({ length: 4 }).map(() => `
        <div class="roadmap-level-card skeleton-card">
            <div class="skeleton-line wide"></div>
            <div class="skeleton-line"></div>
            <div class="skeleton-line short"></div>
        </div>
    `).join('');
}

function renderRoadmapLevels(levels) {
    const container = document.getElementById('roadmapLevels');
    if (!container) return;
    container.innerHTML = levels.map(level => {
        const locked = level.status === 'locked';
        return `
            <div class="roadmap-level-card ${escapeHtml(level.status)} ${level.isSelected ? 'selected' : ''}">
                <div class="roadmap-level-top">
                    <div class="roadmap-level-icon"><i class="fas fa-${escapeAttr(level.icon || 'route')}"></i></div>
                    <span class="roadmap-status-pill ${escapeHtml(level.status)}">${level.isSelected ? 'Selected' : locked ? 'Locked' : level.status === 'completed' ? 'Completed' : 'Open'}</span>
                </div>
                <div class="roadmap-level-main">
                    <h3>${escapeHtml(level.title)}</h3>
                    <p>${escapeHtml(level.description)}</p>
                    <div class="roadmap-meta">${escapeHtml(level.target)} · ${level.completedLessons || 0}/${level.lessonCount || 0} lessons</div>
                    <div class="roadmap-progress"><span style="width:${level.progressPercent || 0}%"></span></div>
                    <div class="roadmap-percent">${level.progressPercent || 0}% complete</div>
                </div>
                <button class="btn btn-primary" ${locked ? 'disabled' : ''} onclick="loadRoadmapLevel('${level.id}')">
                    <i class="fas fa-play"></i> ${level.progressPercent ? 'Continue' : 'Start'}
                </button>
            </div>
        `;
    }).join('');
}

async function loadRoadmapLevels() {
    const container = document.getElementById('roadmapLevels');
    const detail = document.getElementById('roadmapDetail');
    if (!container) return;
    container.classList.remove('hidden');
    container.innerHTML = renderRoadmapSkeleton();
    if (detail) detail.classList.add('hidden');
    try {
        const userParam = state.currentUser?.id ? `?user_id=${state.currentUser.id}` : '';
        const now = Date.now();
        if (state.roadmapCache && now - state.roadmapCacheAt < 45000) {
            renderRoadmapLevels(state.roadmapCache.levels || []);
            return;
        }
        const response = await fetch(`/api/roadmap/levels${userParam}`);
        const data = await response.json();
        if (!data.success) throw new Error(data.error || 'Roadmap error');
        state.roadmapCache = data;
        state.roadmapCacheAt = now;
        renderRoadmapLevels(data.levels || []);
    } catch (error) {
        console.error('Roadmap load error:', error);
        container.innerHTML = '<p>Khong tai duoc lo trinh hoc.</p>';
    }
}

async function openSavedRoadmap() {
    const savedLevel = state.currentUser?.selected_roadmap_level || state.selectedRoadmapLevelId || localStorage.getItem('selectedRoadmapLevelId');
    if (savedLevel) {
        const loaded = await loadRoadmapLevel(savedLevel, { persist: false, fallbackToList: true });
        if (loaded) return;
    }
    await loadRoadmapLevels();
}

async function saveRoadmapSelection(levelId) {
    state.selectedRoadmapLevelId = levelId;
    localStorage.setItem('selectedRoadmapLevelId', levelId);
    if (!state.currentUser?.id) return;
    try {
        const response = await fetch('/api/roadmap/selection', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: state.currentUser.id, level_id: levelId })
        });
        const data = await response.json();
        if (data.success && data.user) {
            state.currentUser = data.user;
        }
    } catch (error) {
        console.error('Save roadmap selection error:', error);
    }
}

async function loadRoadmapLevel(levelId, options = {}) {
    state.selectedRoadmapLevelId = levelId;
    if (options.persist !== false) saveRoadmapSelection(levelId);
    const detail = document.getElementById('roadmapDetail');
    const container = document.getElementById('roadmapLevels');
    if (!detail) return;
    if (container) container.classList.add('hidden');
    detail.classList.remove('hidden');
    detail.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>Dang tai bai hoc...</p></div>';
    let level;
    try {
        const userParam = state.currentUser?.id ? `?user_id=${state.currentUser.id}` : '';
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 12000);
        const response = await fetch(`/api/roadmap/levels/${levelId}${userParam}`, { signal: controller.signal });
        clearTimeout(timer);
        const data = await response.json().catch(() => ({}));
        if (!response.ok || !data.success || !data.level) {
            throw new Error(data.error || `Roadmap level load failed (${response.status})`);
        }
        level = data.level;
    } catch (error) {
        console.error('Roadmap level load error:', error);
        if (options.fallbackToList) {
            localStorage.removeItem('selectedRoadmapLevelId');
            state.selectedRoadmapLevelId = null;
            showToast('⚠️', 'Lo trinh da luu chua tai duoc. Vui long chon lai.');
            await loadRoadmapLevels();
            return false;
        }
        detail.innerHTML = `
            <div class="roadmap-error-state">
                <p>Khong tai duoc bai hoc trong lo trinh nay.</p>
                <button class="btn btn-secondary" onclick="loadRoadmapLevels()">Chon lo trinh khac</button>
            </div>
        `;
        return false;
    }
    renderRoadmapDashboard(level.dashboard);
    detail.innerHTML = `
        <div class="roadmap-detail-header">
            <button class="btn btn-secondary" onclick="loadRoadmapLevels()"><i class="fas fa-arrow-left"></i> Chon lo trinh khac</button>
            <h3><i class="fas fa-${escapeAttr(level.icon || 'route')}"></i> ${escapeHtml(level.title)}</h3>
            <p>${escapeHtml(level.description)}</p>
        </div>
        ${level.units.map(unit => `
            <div class="roadmap-unit ${escapeHtml(unit.status)}">
                <div class="roadmap-unit-header">
                    <div>
                        <h4>${escapeHtml(unit.title)}</h4>
                        <p>${escapeHtml(unit.description)}</p>
                    </div>
                    <span>${unit.completedLessons || 0}/${unit.lessonCount || 0}</span>
                </div>
                <div class="roadmap-progress"><span style="width:${unit.progressPercent || 0}%"></span></div>
                <div class="roadmap-lessons">
                    ${unit.lessons.map(lesson => `
                        <button class="roadmap-lesson ${escapeHtml(lesson.status)}" ${lesson.status === 'locked' ? 'disabled' : ''} onclick="openRoadmapLesson('${lesson.id}')">
                            <i class="fas fa-${escapeAttr(lesson.icon || 'book')}"></i>
                            <span>${escapeHtml(lesson.title)}</span>
                            <small>${lesson.status} · ${lesson.type}${lesson.isAiEnabled ? ' · AI optional' : ''}</small>
                        </button>
                    `).join('')}
                </div>
            </div>
        `).join('')}
    `;
    detail.scrollIntoView({ behavior: 'smooth', block: 'start' });
    return true;
}

async function openRoadmapLesson(lessonId) {
    const userParam = state.currentUser?.id ? `?user_id=${state.currentUser.id}` : '';
    const response = await fetch(`/api/roadmap/lessons/${lessonId}${userParam}`);
    const data = await response.json();
    if (!data.success) {
        showToast('🔒', data.error || 'Lesson is locked');
        return;
    }
    const lesson = data.lesson;
    state.currentRoadmapLesson = lesson;
    const detail = document.getElementById('roadmapDetail');
    detail.innerHTML = `
        <div class="roadmap-lesson-view">
            <button class="btn btn-secondary" onclick="loadRoadmapLevel('${lesson.levelId}')">Quay lai unit</button>
            <h3>${escapeHtml(lesson.title)}</h3>
            <div class="roadmap-content-block">${renderRoadmapContent(lesson)}</div>
            <div class="roadmap-actions">
                ${lesson.isAiEnabled && lesson.type !== 'speaking' ? `<button class="btn btn-stats" onclick="logRoadmapAiUse('${lesson.aiFeatureType}', '${lesson.id}')"><i class="fas fa-wand-magic-sparkles"></i> AI giai thich giup toi</button>` : ''}
                <button class="btn btn-primary" onclick="completeRoadmapLesson('${lesson.id}', '${lesson.levelId}')"><i class="fas fa-check"></i> Hoan thanh bai</button>
            </div>
        </div>
    `;
}

function renderRoadmapContent(lesson) {
    const content = lesson.content || {};
    if (lesson.type === 'integrated') {
        const vocab = content.vocabulary || [];
        const patterns = content.sentencePatterns || [];
        const grammar = content.grammar || [];
        const dialogue = content.dialogue || [];
        const speaking = content.speaking || [];
        const quiz = content.quiz || [];
        const review = content.review || [];
        return `
            <div class="lesson-app-card">
                <div class="lesson-section-header"><i class="fas fa-spell-check"></i><h4>Vocabulary</h4></div>
                <div class="roadmap-vocab">${vocab.map(w => `
                    <div class="vocab-tile">
                        <strong>${escapeHtml(w.word)}</strong>
                        <span>${escapeHtml(w.meaning)}</span>
                        <small>${escapeHtml(w.example)}</small>
                        <div>
                            <button class="speak-btn" onclick="playSmartAudio('${escapeAttr(w.word)}', '${escapeAttr(w.audioUrl || '')}')"><i class="fas fa-volume-up"></i></button>
                            <button class="speak-btn" onclick="playSmartAudio('${escapeAttr(w.example)}')"><i class="fas fa-comment-dots"></i></button>
                        </div>
                    </div>
                `).join('')}</div>
            </div>
            <div class="lesson-app-card">
                <div class="lesson-section-header"><i class="fas fa-layer-group"></i><h4>Sentence Patterns</h4></div>
                ${patterns.map(p => `<p class="pattern-line">${escapeHtml(p)} <button class="speak-btn" onclick="playSmartAudio('${escapeAttr(p)}')"><i class="fas fa-volume-up"></i></button></p>`).join('')}
            </div>
            <div class="lesson-app-card">
                <div class="lesson-section-header"><i class="fas fa-diagram-project"></i><h4>Grammar Mini</h4></div>
                <ul>${grammar.map(rule => `<li>${escapeHtml(rule)}</li>`).join('')}</ul>
            </div>
            <div class="lesson-app-card">
                <div class="lesson-section-header"><i class="fas fa-headphones"></i><h4>Sample Dialogue</h4></div>
                <div class="audio-toolbar">
                    <button class="btn btn-audio" onclick="playDialogueSmart(false)"><i class="fas fa-play"></i> Play dialogue</button>
                    <button class="btn btn-secondary" onclick="playDialogueSmart(true)"><i class="fas fa-gauge-low"></i> Slow 0.8x</button>
                    <button class="btn btn-secondary" onclick="repeatDialogueSmart()"><i class="fas fa-repeat"></i> Repeat</button>
                </div>
                ${dialogue.map(line => `<p class="dialogue-app-line"><strong>${escapeHtml(line.speaker)}:</strong> ${escapeHtml(line.text)} <button class="speak-btn" onclick="playSmartAudio('${escapeAttr(line.text)}')"><i class="fas fa-volume-up"></i></button></p>`).join('')}
            </div>
            <div class="lesson-app-card">
                <div class="lesson-section-header"><i class="fas fa-microphone-lines"></i><h4>Speaking Practice</h4></div>
                <div class="speaking-practice-panel">
                    ${speaking.map(item => {
                        const sentence = item.text || item;
                        return `
                            <div class="speaking-line">
                                <strong>${escapeHtml(sentence)}</strong>
                                <div class="speaking-line-actions">
                                    <button class="btn btn-audio" onclick="startRoadmapSpeaking('${escapeAttr(sentence)}')"><i class="fas fa-volume-up"></i> Listen</button>
                                    <button class="btn btn-record" onclick="recordRoadmapSpeaking('${escapeAttr(sentence)}')"><i class="fas fa-microphone"></i> Record</button>
                                    <button class="btn btn-secondary" onclick="startShadowing('${escapeAttr(sentence)}')"><i class="fas fa-person-running"></i> Shadow</button>
                                </div>
                            </div>
                        `;
                    }).join('')}
                    <div id="roadmapSpeakingResult" class="speaking-result hidden"></div>
                </div>
            </div>
            <div class="lesson-app-card">
                <div class="lesson-section-header"><i class="fas fa-circle-question"></i><h4>Quiz</h4></div>
                ${quiz.map(q => `<div class="roadmap-quiz"><strong>${escapeHtml(q.question)}</strong><div>${(q.options || []).map(o => `<button class="btn btn-secondary" onclick="this.closest('.roadmap-quiz').querySelector('em').textContent='Answer: ${escapeHtml(q.answer)}'">${escapeHtml(o)}</button>`).join(' ')}</div><em></em></div>`).join('')}
            </div>
            <div class="lesson-app-card">
                <div class="lesson-section-header"><i class="fas fa-rotate-right"></i><h4>Review</h4></div>
                <ul>${review.map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
            </div>
        `;
    }
    if (lesson.type === 'vocabulary') {
        return `<div class="roadmap-vocab">${(content.words || []).map(w => `
            <div><strong>${escapeHtml(w.word)}</strong>: ${escapeHtml(w.meaning)}
            <button class="speak-btn" onclick="playRoadmapAudio('${escapeAttr(w.word)}')"><i class="fas fa-volume-up"></i></button>
            <br><small>${escapeHtml(w.example)}</small>
            <button class="speak-btn" onclick="playRoadmapAudio('${escapeAttr(w.example)}')"><i class="fas fa-play"></i></button></div>
        `).join('')}</div>`;
    }
    if (lesson.type === 'grammar') {
        return `<ul>${(content.rules || []).map(rule => `<li>${escapeHtml(rule)}</li>`).join('')}</ul><div>${(content.examples || []).map(ex => `<p>${escapeHtml(ex)} <button class="speak-btn" onclick="playRoadmapAudio('${escapeAttr(ex)}')"><i class="fas fa-volume-up"></i></button></p>`).join('')}</div>`;
    }
    if (lesson.type === 'quiz') {
        return (content.questions || []).map(q => `<div class="roadmap-quiz"><strong>${escapeHtml(q.question)}</strong><div>${(q.options || []).map(o => `<button class="btn btn-secondary" onclick="this.closest('.roadmap-quiz').querySelector('em').textContent='Dap an: ${escapeHtml(q.answer)}'">${escapeHtml(o)}</button>`).join(' ')}</div><em></em></div>`).join('');
    }
    if (lesson.type === 'listening') {
        return `
            <div class="audio-toolbar">
                <button class="btn btn-audio" onclick="playFullRoadmapLesson(false)"><i class="fas fa-headphones"></i> Play full</button>
                <button class="btn btn-secondary" onclick="playFullRoadmapLesson(true)"><i class="fas fa-repeat"></i> Repeat slow</button>
            </div>
            ${(content.dialogue || []).map(line => `<p><strong>${escapeHtml(line.speaker)}:</strong> ${escapeHtml(line.text)} <button class="speak-btn" onclick="playRoadmapAudio('${escapeAttr(line.text)}')"><i class="fas fa-volume-up"></i></button></p>`).join('')}
        `;
    }
    if (lesson.type === 'speaking') {
        const practice = content.practice || [];
        return `
            <div class="speaking-practice-panel">
                ${practice.map(sentence => `
                    <div class="speaking-line">
                        <strong>${escapeHtml(sentence)}</strong>
                        <div class="speaking-line-actions">
                            <button class="btn btn-audio" onclick="startRoadmapSpeaking('${escapeAttr(sentence)}')"><i class="fas fa-volume-up"></i> Listen</button>
                            <button class="btn btn-record" onclick="recordRoadmapSpeaking('${escapeAttr(sentence)}')"><i class="fas fa-microphone"></i> Record</button>
                            <button class="btn btn-secondary" onclick="startShadowing('${escapeAttr(sentence)}')"><i class="fas fa-person-running"></i> Shadow</button>
                        </div>
                    </div>
                `).join('')}
                <div id="roadmapSpeakingResult" class="speaking-result hidden"></div>
            </div>
        `;
    }
    return `<pre>${escapeHtml(JSON.stringify(content, null, 2))}</pre>`;
}

async function completeRoadmapLesson(lessonId, levelId) {
    if (state.currentUser) {
        const response = await fetch('/api/roadmap/progress', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: state.currentUser.id, lesson_id: lessonId, status: 'completed' })
        });
        const data = await response.json();
        if (!data.success) {
            showToast('🔒', data.error || 'Bai hoc dang khoa');
            return;
        }
        if (data.dashboard) renderRoadmapDashboard(data.dashboard);
    }
    state.roadmapCache = null;
    showToast('✅', 'Da luu tien do bai hoc');
    loadRoadmapLevel(levelId);
}

async function logRoadmapAiUse(featureType, lessonId = null) {
    const response = await fetch(lessonId ? '/api/roadmap/ai/explain' : '/api/ai/usage/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            userId: state.currentUser?.id || null,
            user_id: state.currentUser?.id || null,
            featureType,
            feature_type: featureType,
            lesson_id: lessonId,
            tokenUsed: 80,
            estimatedCost: 0
        })
    });
    const data = await response.json();
    showToast(data.success ? '??' : '??', data.success ? `AI ${featureType}: ${data.limit.used}/${data.limit.limit} hom nay` : data.error);
    if (data.success && data.explanation) {
        const block = document.querySelector('.roadmap-content-block');
        if (block) {
            block.insertAdjacentHTML('beforeend', `<div class="roadmap-ai-explanation"><h4>AI Coach</h4><pre>${escapeHtml(data.explanation)}</pre></div>`);
        }
    }
}

function renderRoadmapDashboard(dashboard = {}) {
    const modalBody = document.querySelector('#roadmapModal .modal-body');
    if (!modalBody) return;
    let panel = document.getElementById('roadmapDashboardPanel');
    if (!panel) {
        panel = document.createElement('div');
        panel.id = 'roadmapDashboardPanel';
        panel.className = 'roadmap-dashboard-panel';
        modalBody.insertBefore(panel, modalBody.firstChild);
    }
    const goal = dashboard.dailyGoalXP || 50;
    const daily = Math.min(dashboard.dailyProgressXP || 0, goal);
    const percent = Math.round((daily / goal) * 100);
    panel.innerHTML = `
        <div class="roadmap-stat"><strong>${dashboard.totalXP || 0}</strong><span>XP</span></div>
        <div class="roadmap-stat"><strong>${dashboard.streakDays || 0}</strong><span>day streak</span></div>
        <div class="roadmap-stat daily-goal">
            <strong>${daily}/${goal}</strong><span>daily goal</span>
            <div class="roadmap-progress"><span style="width:${percent}%"></span></div>
        </div>
        <div class="roadmap-badges">
            ${(dashboard.badges || []).slice(-3).map(b => `<span><i class="fas fa-award"></i> ${escapeHtml(b.title)}</span>`).join('') || '<span>No badges yet</span>'}
        </div>
        <div class="mission-panel">
            <h4>Daily Missions</h4>
            ${(dashboard.dailyMissions || []).map(m => {
                const done = (m.current || 0) >= (m.target || 1);
                const pct = Math.min(100, Math.round(((m.current || 0) / (m.target || 1)) * 100));
                return `<div class="mission-row ${done ? 'done' : ''}">
                    <div><strong>${escapeHtml(m.title)}</strong><span>${m.current || 0}/${m.target || 0} · +${m.rewardXP || 0} XP</span></div>
                    <div class="roadmap-progress"><span style="width:${pct}%"></span></div>
                </div>`;
            }).join('')}
        </div>
        <div class="mission-panel weekly">
            <h4>Weekly Challenge</h4>
            ${(dashboard.weeklyChallenge || []).map(m => {
                const done = (m.current || 0) >= (m.target || 1);
                const pct = Math.min(100, Math.round(((m.current || 0) / (m.target || 1)) * 100));
                return `<div class="mission-row ${done ? 'done' : ''}">
                    <div><strong>${escapeHtml(m.title)}</strong><span>${m.current || 0}/${m.target || 0} · +${m.rewardXP || 0} XP</span></div>
                    <div class="roadmap-progress"><span style="width:${pct}%"></span></div>
                </div>`;
            }).join('')}
        </div>
        <div class="continue-card">
            <strong>Continue Learning</strong>
            <span>${escapeHtml(dashboard.continueLesson?.title || 'Start your first lesson')}</span>
            <button class="btn btn-primary" onclick="continueRoadmapLesson()"><i class="fas fa-play"></i> Continue</button>
        </div>
    `;
    if ((dashboard.streakDays || 0) >= 3 && !sessionStorage.getItem('streak_popup_seen')) {
        sessionStorage.setItem('streak_popup_seen', '1');
        showToast('🔥', `You are on a ${dashboard.streakDays}-day streak!`);
    }
}

async function continueRoadmapLesson() {
    const userParam = state.currentUser?.id ? `?user_id=${state.currentUser.id}` : '';
    const response = await fetch(`/api/roadmap/continue${userParam}`);
    const data = await response.json();
    if (data.success && data.lesson) {
        await loadRoadmapLevel(data.lesson.levelId);
        await openRoadmapLesson(data.lesson.id);
    } else {
        loadRoadmapLevels();
    }
}

function playRoadmapAudio(text, slow = false) {
    speakText(text, slow ? 0.7 : 1.0);
}

function playSmartAudio(text, audioUrl = '', options = {}) {
    const slow = Boolean(options.slow);
    const repeat = Boolean(options.repeat);
    if (audioUrl && audioUrl.trim()) {
        const cached = state.audioCache.get(audioUrl) || new Audio(audioUrl);
        state.audioCache.set(audioUrl, cached);
        cached.playbackRate = slow ? 0.8 : 1.0;
        cached.currentTime = 0;
        cached.onended = repeat ? () => {
            cached.currentTime = 0;
            cached.play().catch(() => speakText(text, slow ? 0.8 : 1.0));
        } : null;
        cached.play().catch(() => speakText(text, slow ? 0.8 : 1.0));
        return;
    }
    speakText(text, slow ? 0.8 : 1.0);
    if (repeat) {
        setTimeout(() => speakText(text, slow ? 0.8 : 1.0), Math.max(1600, String(text).length * 70));
    }
}

function getCurrentDialogueText() {
    const dialogue = state.currentRoadmapLesson?.content?.dialogue || [];
    return dialogue.map(line => line.text).join(' ');
}

function playDialogueSmart(slow = false) {
    const text = getCurrentDialogueText();
    const audioUrl = state.currentRoadmapLesson?.audio?.dialogueUrl || state.currentRoadmapLesson?.audioUrl || '';
    playSmartAudio(text, audioUrl, { slow });
}

function repeatDialogueSmart() {
    const text = getCurrentDialogueText();
    const audioUrl = state.currentRoadmapLesson?.audio?.dialogueUrl || state.currentRoadmapLesson?.audioUrl || '';
    playSmartAudio(text, audioUrl, { repeat: true });
}

function playFullRoadmapLesson(slow = false) {
    const lesson = state.currentRoadmapLesson;
    if (!lesson) return;
    const dialogue = lesson.content?.dialogue || [];
    const text = dialogue.map(line => line.text).join(' ');
    playRoadmapAudio(text, slow);
}

function startRoadmapSpeaking(sentence) {
    state.currentSpeakingExpected = sentence;
    state.currentSpeakingTranscript = '';
    playRoadmapAudio(sentence);
    const result = document.getElementById('roadmapSpeakingResult');
    if (result) {
        result.classList.remove('hidden');
        result.innerHTML = `<div class="speaking-flow">Listen, then press Record when ready.</div>`;
    }
}

async function recordRoadmapSpeaking(sentence) {
    state.currentSpeakingExpected = sentence;
    const result = document.getElementById('roadmapSpeakingResult');
    if (result) {
        result.classList.remove('hidden');
        result.innerHTML = '<div class="record-countdown">3</div><div class="record-hint">Get ready...</div>';
    }
    await runRecordCountdown(result);
    await captureUserAudio();
    if (!state.recognition) {
        renderRoadmapSpeakingResult('', sentence, 'Speech recognition is not supported in this browser. You can still listen and repeat out loud.');
        return;
    }
    state.isRoadmapSpeakingMode = true;
    state.recognition.lang = 'en-US';
    state.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        state.currentSpeakingTranscript = transcript;
        state.isRoadmapSpeakingMode = false;
        renderRoadmapSpeakingResult(transcript, sentence);
        setTimeout(initializeSpeechRecognition, 0);
    };
    state.recognition.onerror = () => {
        state.isRoadmapSpeakingMode = false;
        renderRoadmapSpeakingResult('', sentence, 'Could not hear clearly. Try again in Chrome or Edge.');
        setTimeout(initializeSpeechRecognition, 0);
    };
    try {
        if (result) result.innerHTML = '<div class="record-waveform"><span></span><span></span><span></span><span></span><span></span></div><div class="record-hint">Recording... speak naturally.</div>';
        state.recognition.start();
    } catch (error) {
        renderRoadmapSpeakingResult('', sentence, 'Microphone is already active. Please try again.');
    }
}

function runRecordCountdown(container) {
    return new Promise(resolve => {
        let count = 3;
        const tick = () => {
            if (container) {
                container.innerHTML = `<div class="record-countdown">${count}</div><div class="record-hint">Get ready...</div>`;
            }
            count -= 1;
            if (count <= 0) {
                setTimeout(resolve, 350);
            } else {
                setTimeout(tick, 650);
            }
        };
        tick();
    });
}

async function captureUserAudio() {
    if (!navigator.mediaDevices || !window.MediaRecorder) return;
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        state.recordedChunks = [];
        state.mediaRecorder = new MediaRecorder(stream);
        state.mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) state.recordedChunks.push(event.data);
        };
        state.mediaRecorder.onstop = () => {
            const blob = new Blob(state.recordedChunks, { type: 'audio/webm' });
            if (state.currentUserAudioUrl) URL.revokeObjectURL(state.currentUserAudioUrl);
            state.currentUserAudioUrl = URL.createObjectURL(blob);
            stream.getTracks().forEach(track => track.stop());
        };
        state.mediaRecorder.start();
        setTimeout(() => {
            if (state.mediaRecorder && state.mediaRecorder.state === 'recording') {
                state.mediaRecorder.stop();
            }
        }, 5500);
    } catch (error) {
        console.warn('Audio recording unavailable:', error);
    }
}

function startShadowing(sentence) {
    startRoadmapSpeaking(sentence);
    setTimeout(() => recordRoadmapSpeaking(sentence), 2000);
}

function compareSpeech(expected, spoken) {
    const clean = value => String(value || '').toLowerCase().replace(/[^\w\s']/g, '').split(/\s+/).filter(Boolean);
    const expectedWords = clean(expected);
    const spokenWords = clean(spoken);
    const missing = expectedWords.filter(word => !spokenWords.includes(word));
    const extra = spokenWords.filter(word => !expectedWords.includes(word));
    const correct = expectedWords.filter(word => spokenWords.includes(word)).length;
    const accuracy = expectedWords.length ? Math.round((correct / expectedWords.length) * 100) : 0;
    const completeness = expectedWords.length ? Math.round(((expectedWords.length - missing.length) / expectedWords.length) * 100) : 0;
    const lengthRatio = expectedWords.length ? Math.min(spokenWords.length, expectedWords.length) / expectedWords.length : 0;
    const fluency = Math.round(Math.max(0, Math.min(100, (lengthRatio * 75) + (extra.length ? -10 : 15))));
    const expectedMarkup = expectedWords.map(word => {
        const cls = spokenWords.includes(word) ? 'word-ok' : 'word-missing';
        return `<span class="${cls}">${escapeHtml(word)}</span>`;
    }).join(' ');
    const spokenMarkup = spokenWords.map(word => {
        const cls = expectedWords.includes(word) ? 'word-ok' : 'word-wrong';
        return `<span class="${cls}">${escapeHtml(word)}</span>`;
    }).join(' ');
    return { missing, extra, score: accuracy, accuracy, fluency, completeness, expectedMarkup, spokenMarkup };
}

function renderRoadmapSpeakingResult(transcript, expected, fallback = '') {
    const result = document.getElementById('roadmapSpeakingResult');
    if (!result) return;
    const feedback = compareSpeech(expected, transcript);
    result.classList.remove('hidden');
    result.innerHTML = `
        <div class="pronunciation-feedback">
            <div class="feedback-title">Speaking result</div>
            <p><strong>Expected:</strong> <span class="speech-compare">${feedback.expectedMarkup}</span></p>
            <p><strong>You said:</strong> <span class="speech-compare">${transcript ? feedback.spokenMarkup : escapeHtml(fallback || 'No transcript')}</span></p>
            <div class="speaking-score-grid">
                <div><strong>${feedback.accuracy}%</strong><span>Accuracy</span></div>
                <div><strong>${feedback.fluency}%</strong><span>Fluency</span></div>
                <div><strong>${feedback.completeness}%</strong><span>Completeness</span></div>
            </div>
            ${feedback.missing.length ? `<div class="feedback-item missing">Missing: ${feedback.missing.map(escapeHtml).join(', ')}</div>` : ''}
            ${feedback.extra.length ? `<div class="feedback-item">Extra/different: ${feedback.extra.map(escapeHtml).join(', ')}</div>` : ''}
            ${state.currentUserAudioUrl ? `<audio controls src="${state.currentUserAudioUrl}"></audio>` : ''}
            <div class="speaking-line-actions">
                <button class="btn btn-audio" onclick="playRoadmapAudio('${escapeAttr(expected)}', true)"><i class="fas fa-volume-up"></i> Slow sample</button>
                <button class="btn btn-record" onclick="recordRoadmapSpeaking('${escapeAttr(expected)}')"><i class="fas fa-rotate-right"></i> Retry</button>
                <button class="btn btn-stats" onclick="requestAiSpeakingCorrection()"><i class="fas fa-wand-magic-sparkles"></i> AI sua phat am cho toi</button>
            </div>
            <div id="aiSpeakingCorrection"></div>
        </div>
    `;
}

async function requestAiSpeakingCorrection() {
    if (!state.currentSpeakingExpected || !state.currentSpeakingTranscript) {
        showToast('⚠️', 'Hay ghi am va co transcript truoc khi goi AI.');
        return;
    }
    const target = document.getElementById('aiSpeakingCorrection');
    if (target) target.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>AI dang sua...</p></div>';
    const response = await fetch('/api/roadmap/ai/speaking-correction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: state.currentUser?.id || null,
            lesson_id: state.currentRoadmapLesson?.id || null,
            expected: state.currentSpeakingExpected,
            transcript: state.currentSpeakingTranscript
        })
    });
    const data = await response.json();
    if (!data.success) {
        if (target) target.innerHTML = `<p>${escapeHtml(data.error || 'AI error')}</p>`;
        return;
    }
    const c = data.correction || {};
    if (target) {
        target.innerHTML = `
            <div class="roadmap-ai-explanation">
                <h4>AI Speaking Coach</h4>
                <p>Overall: ${c.overall_score || 0}/100 · Pronunciation: ${c.pronunciation_score || 0}/100 · Grammar: ${c.grammar_score || 0}/100</p>
                <p>${escapeHtml(c.short_feedback || '')}</p>
                <p><strong>Suggested:</strong> ${escapeHtml(c.suggested_sentence || '')}</p>
            </div>
        `;
    }
    showToast('🤖', `AI used ${data.limit.used}/${data.limit.limit} today`);
}

async function startPlacementTest() {
    const detail = document.getElementById('roadmapDetail');
    if (!detail) return;
    detail.classList.remove('hidden');
    detail.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>Dang tai test...</p></div>';
    const response = await fetch('/api/placement-test');
    const data = await response.json();
    if (!data.success) {
        detail.innerHTML = '<p>Khong tai duoc test dau vao.</p>';
        return;
    }
    detail.innerHTML = `
        <div class="placement-test">
            <h3>Placement Test</h3>
            ${data.questions.map((q, idx) => `
                <div class="placement-question">
                    <strong>${idx + 1}. ${escapeHtml(q.question)}</strong>
                    <div>
                        ${q.options.map(option => `
                            <label><input type="radio" name="placement_${q.id}" value="${escapeHtml(option)}"> ${escapeHtml(option)}</label>
                        `).join('')}
                    </div>
                </div>
            `).join('')}
            <button class="btn btn-primary" onclick="submitPlacementTest()">Xem goi y level</button>
        </div>
    `;
}

async function submitPlacementTest() {
    const answers = {};
    document.querySelectorAll('.placement-question input:checked').forEach(input => {
        answers[input.name.replace('placement_', '')] = input.value;
    });
    const response = await fetch('/api/placement-test/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers })
    });
    const data = await response.json();
    const detail = document.getElementById('roadmapDetail');
    if (!data.success || !detail) return;
    const result = data.result;
    detail.innerHTML = `
        <div class="placement-result">
            <h3>Ket qua: ${result.correct}/${result.total} (${result.percent}%)</h3>
            <p>App goi y level: <strong>${escapeHtml(result.recommendedLevel.title)}</strong></p>
            <p>${escapeHtml(result.recommendedLevel.description)}</p>
            <button class="btn btn-primary" onclick="loadRoadmapLevel('${result.recommendedLevelId}')">Bat dau level nay</button>
        </div>
    `;
}


// ==========================================
// Speaking Practice
// ==========================================
function openSpeakingPractice(index) {
    if (!state.currentLesson || !state.currentLesson.practice) return;
    
    state.currentPracticeIndex = index;
    const sentence = state.currentLesson.practice[index];
    
    elements.practiceText.textContent = sentence;
    elements.speakingResult.classList.add('hidden');
    elements.speakingResult.innerHTML = '';
    
    closeModal('lessonModal');
    openModal('speakingModal');
    
    // Tự động đọc câu
    setTimeout(() => speakText(sentence), 500);
}

function togglePracticeRecording() {
    if (!state.recognition) {
        showToast('❌', 'Trình duyệt không hỗ trợ nhận diện giọng nói.');
        return;
    }
    
    if (state.isRecording) {
        stopPracticeRecording();
    } else {
        startPracticeRecording();
    }
}

function startPracticeRecording() {
    state.isRecording = true;
    state.isPracticeMode = true;
    elements.recordPracticeBtn.classList.add('recording');
    elements.recordPracticeBtn.innerHTML = '<i class="fas fa-stop"></i> Dừng';
    
    try {
        state.recognition.start();
    } catch (error) {
        console.error('Practice recording error:', error);
        stopPracticeRecording();
    }
}

function stopPracticeRecording() {
    state.isRecording = false;
    state.isPracticeMode = false;
    elements.recordPracticeBtn.classList.remove('recording');
    elements.recordPracticeBtn.innerHTML = '<i class="fas fa-microphone"></i> Bấm để nói';
    
    try {
        state.recognition.stop();
    } catch (error) {
        // Ignore
    }
}

async function evaluatePracticeSpeech(spokenText) {
    stopPracticeRecording();
    
    const expectedText = state.currentLesson.practice[state.currentPracticeIndex];
    
    // Hiển thị loading
    elements.speakingResult.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>Cô đang nghe...</p></div>';
    elements.speakingResult.classList.remove('hidden');
    
    try {
        const response = await fetch('/api/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                spoken: spokenText,
                expected: expectedText
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            renderEvaluation(data.evaluation, spokenText, expectedText);
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        elements.speakingResult.innerHTML = `
            <div class="result-wrong">❌ Không đánh giá được</div>
            <div class="result-feedback">Em thử lại sau nhé!</div>
        `;
    }
}

function renderEvaluation(evaluation, spoken, expected) {
    const isCorrect = evaluation.correct;
    
    let html = '';
    
    if (isCorrect) {
        html += `<div class="result-correct">✅ Chính xác! Giỏi lắm em!</div>`;
    } else {
        html += `<div class="result-wrong">❌ Gần đúng rồi!</div>`;
    }
    
    html += `<div class="result-feedback">${evaluation.feedback}</div>`;
    
    if (!isCorrect && evaluation.correction) {
        html += `
            <div style="margin-top: 15px; padding: 15px; background: #fff; border-radius: 10px;">
                <div><strong>Em nói:</strong> ${spoken}</div>
                <div style="margin-top: 8px;"><strong>Đúng là:</strong> ${evaluation.correction}</div>
            </div>
        `;
    }
    
    if (evaluation.suggestion && evaluation.suggestion !== expected) {
        html += `
            <div style="margin-top: 10px; color: #666; font-style: italic;">
                💡 Gợi ý: ${evaluation.suggestion}
            </div>
        `;
    }
    
    // Add buttons
    html += `
        <div style="margin-top: 20px; display: flex; gap: 10px; justify-content: center;">
            <button class="btn btn-audio" onclick="speakText('${expected.replace(/'/g, "\\'")}')">
                <i class="fas fa-volume-up"></i> Nghe lại
            </button>
            <button class="btn btn-lesson" onclick="closeModal('speakingModal'); openModal('lessonModal');">
                <i class="fas fa-arrow-left"></i> Quay lại
            </button>
        </div>
    `;
    
    elements.speakingResult.innerHTML = html;
}

// ==========================================
// Stats Functions
// ==========================================
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (data.success) {
            const stats = data.stats;
            
            elements.statLessons.textContent = stats.total_lessons;
            elements.statChats.textContent = stats.total_chat_interactions;
            elements.statSpeaking.textContent = stats.total_speaking_practices;
            elements.statDays.textContent = stats.learning_days;
            
            // Render common mistakes
            if (stats.common_mistakes && stats.common_mistakes.length > 0) {
                elements.mistakesList.innerHTML = stats.common_mistakes.map(m => `
                    <li>
                        <span>${m[0]}</span>
                        <span class="mistake-count">${m[1]} lần</span>
                    </li>
                `).join('');
            } else {
                elements.mistakesList.innerHTML = '<li>Chưa có lỗi nào được ghi nhận. Tuyệt vời! 🎉</li>';
            }
        }
    } catch (error) {
        console.error('Stats error:', error);
    }
}

// ==========================================
// Modal Functions
// ==========================================
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        
        // Load content if needed
        if (modalId === 'lessonModal') {
            loadLesson();
        }
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
        
        // Stop any recording when closing
        if (state.isRecording) {
            stopRecording();
            stopPracticeRecording();
        }
    }
}

// ==========================================
// Toast Notification
// ==========================================
function showToast(icon, message) {
    elements.toastIcon.textContent = icon;
    elements.toastMessage.textContent = message;
    elements.toast.classList.remove('hidden');
    
    // Auto hide after 3 seconds
    setTimeout(() => {
        elements.toast.classList.add('hidden');
    }, 3000);
}

// ==========================================
// Roleplay Functions
// ==========================================
function resetRoleplayUI() {
    // Reset UI to setup state
    elements.roleplaySetup.classList.remove('hidden');
    elements.activeRoleplay.classList.add('hidden');
    elements.roleplayAnalysis.classList.add('hidden');
    
    // Clear previous selection
    document.querySelectorAll('.role-btn').forEach(b => b.classList.remove('selected'));
    state.roleplayRole = null;
    state.roleplaySituation = null;
    state.roleplayHistory = [];
    state.currentAIResponse = null;
    state.currentAnalysis = null;
    
    // Clear messages
    if (elements.roleplayMessages) {
        elements.roleplayMessages.innerHTML = '';
    }
    if (elements.roleplayInput) {
        elements.roleplayInput.value = '';
    }
}

async function startRoleplay() {
    // Validate selection
    if (!state.roleplayRole) {
        showToast('⚠️', 'Em chọn người đối thoại trước nhé!');
        return;
    }
    
    // Kiểm tra freemium limit cho guest
    if (state.isGuest) {
        const check = checkGuestLimit('roleplay');
        if (!check.allowed) {
            showLimitModal();
            return;
        }
        incrementGuestLimit('roleplay');
    }
    
    state.roleplaySituation = elements.roleplaySituation.value;
    
    try {
        // Get user name from profile
        const userName = state.userProfile?.name || 'you';
        
        // Start roleplay session
        const response = await fetch('/api/roleplay/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                role: state.roleplayRole,
                situation: state.roleplaySituation,
                user_name: userName
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Switch to active roleplay view
            elements.roleplaySetup.classList.add('hidden');
            elements.activeRoleplay.classList.remove('hidden');
            
            // Update info display
            document.getElementById('roleplayRoleName').textContent = data.role.name;
            document.getElementById('roleplaySituationName').textContent = data.situation.name;
            
            // Show AI greeting
            addRoleplayMessage(data.greeting, 'ai', data.role.name);
            state.currentAIResponse = data.greeting;
            
            // Auto speak greeting
            speakText(data.greeting);
            
            showToast('🎭', `Bắt đầu luyện với ${data.role.name}!`);
        } else {
            showToast('❌', data.error || 'Không thể bắt đầu luyện hội thoại');
        }
        
    } catch (error) {
        console.error('Start roleplay error:', error);
        showToast('❌', 'Có lỗi xảy ra. Em thử lại nhé!');
    }
}

async function sendRoleplayMessage() {
    const message = elements.roleplayInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addRoleplayMessage(message, 'user', 'Bạn');
    elements.roleplayInput.value = '';
    
    // Show loading
    showRoleplayLoading();
    
    try {
        const response = await fetch('/api/roleplay/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        hideRoleplayLoading();
        
        if (data.success) {
            // Add AI response
            addRoleplayMessage(data.ai_response, 'ai', document.getElementById('roleplayRoleName').textContent);
            state.currentAIResponse = data.ai_response;
            
            // Show analysis
            state.currentAnalysis = data.analysis;
            renderRoleplayAnalysis(data.analysis);
            
            // Auto speak AI response
            speakText(data.ai_response);
            
        } else {
            showToast('❌', data.error || 'Không thể gửi tin nhắn');
        }
        
    } catch (error) {
        hideRoleplayLoading();
        console.error('Roleplay chat error:', error);
        showToast('❌', 'Có lỗi kết nối. Em thử lại nhé!');
    }
}

function addRoleplayMessage(content, type, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `roleplay-message ${type}`;
    
    const avatar = type === 'ai' ? '👤' : '🙂';
    
    messageDiv.innerHTML = `
        <div class="roleplay-message-avatar">${avatar}</div>
        <div class="roleplay-message-bubble">${content}</div>
    `;
    
    elements.roleplayMessages.appendChild(messageDiv);
    elements.roleplayMessages.scrollTop = elements.roleplayMessages.scrollHeight;
}

function showRoleplayLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'roleplay-message ai loading';
    loadingDiv.id = 'roleplayLoading';
    loadingDiv.innerHTML = `
        <div class="roleplay-message-avatar">👤</div>
        <div class="roleplay-message-bubble">
            <span class="typing-dots"><span></span><span></span><span></span></span>
        </div>
    `;
    elements.roleplayMessages.appendChild(loadingDiv);
    elements.roleplayMessages.scrollTop = elements.roleplayMessages.scrollHeight;
}

function hideRoleplayLoading() {
    const loading = document.getElementById('roleplayLoading');
    if (loading) loading.remove();
}

function renderRoleplayAnalysis(analysis) {
    if (!analysis) return;
    
    // Get data from new format
    const originalSentence = analysis.original_sentence || '';
    const errors = analysis.errors || [];
    const corrections = analysis.corrections || [];
    const explanations = analysis.explanations_vn || analysis.suggestions || [];
    const betterVersion = analysis.better_version || analysis.practice_sentence || '';
    const grammarScore = analysis.grammar_score || 3;
    const naturalnessScore = analysis.naturalness_score || analysis.naturalness || 3;
    const emotions = analysis.emotions || ['neutral'];
    
    // Build error details
    let errorDetailsHtml = '';
    if (errors.length > 0) {
        errorDetailsHtml = errors.map((err, idx) => {
            const correction = corrections[idx] || '';
            const explanation = explanations[idx] || '';
            return `
                <div style="margin: 8px 0; padding: 8px; background: #fff3cd; border-radius: 6px;">
                    <div style="color: #e74c3c; text-decoration: line-through;">❌ ${err}</div>
                    <div style="color: #27ae60; font-weight: 600;">✔ ${correction}</div>
                    <div style="color: #666; font-size: 0.9rem; margin-top: 4px;">💡 ${explanation}</div>
                </div>
            `;
        }).join('');
    }
    
    // Generate emotion tags
    const emotionTags = emotions.map(emo => {
        const emotionClasses = {
            'confident': 'confident', 'hesitant': 'hesitant', 'friendly': 'friendly',
            'polite': 'polite', 'unclear': 'unclear', 'neutral': 'neutral', 'too formal': 'polite'
        };
        return `<span class="emotion-tag ${emotionClasses[emo] || 'neutral'}">${emo}</span>`;
    }).join('');
    
    // Generate stars
    const grammarStars = '⭐'.repeat(grammarScore) + '☆'.repeat(5 - grammarScore);
    const naturalnessStars = '⭐'.repeat(naturalnessScore) + '☆'.repeat(5 - naturalnessScore);
    
    // Build HTML with new format
    const html = `
        <div class="analysis-title">📊 Phân tích chi tiết</div>
        
        ${originalSentence ? `
        <div class="analysis-section" style="background: #f8f9fa;">
            <div class="analysis-label">📝 Câu của em:</div>
            <div style="font-style: italic; color: #666;">"${originalSentence}"</div>
        </div>
        ` : ''}
        
        ${errors.length > 0 ? `
        <div class="analysis-section">
            <div class="analysis-label">❌ Lỗi cụ thể:</div>
            ${errorDetailsHtml}
        </div>
        ` : `
        <div class="analysis-section" style="background: #d4edda;">
            <div style="color: #155724; font-weight: 600;">✅ Câu này đúng ngữ pháp!</div>
        </div>
        `}
        
        <div class="analysis-section">
            <div class="analysis-label">✨ Cách nói tự nhiên hơn:</div>
            <div style="font-weight: 600; color: var(--primary-dark); font-size: 1.1rem;">
                "${betterVersion}"
            </div>
            <button onclick="speakText('${betterVersion.replace(/'/g, "\\'")}')" 
                    style="margin-top: 8px; padding: 6px 12px; background: var(--primary-color); 
                           color: white; border: none; border-radius: 4px; cursor: pointer;">
                🔊 Nghe cách nói đúng
            </button>
        </div>
        
        <div class="analysis-section">
            <div class="analysis-label">🔁 Em thử nói lại câu này:</div>
            <div style="color: #666; font-size: 0.9rem;">Nhấn micro và nói theo câu trên để luyện!</div>
        </div>
        
        <div style="display: flex; gap: 15px; flex-wrap: wrap;">
            <div class="analysis-section" style="flex: 1; min-width: 150px;">
                <div class="analysis-label">Ngữ pháp:</div>
                <div class="naturalness-score">
                    <span class="naturalness-stars">${grammarStars}</span>
                    <span>${grammarScore}/5</span>
                </div>
            </div>
            <div class="analysis-section" style="flex: 1; min-width: 150px;">
                <div class="analysis-label">Tự nhiên:</div>
                <div class="naturalness-score">
                    <span class="naturalness-stars">${naturalnessStars}</span>
                    <span>${naturalnessScore}/5</span>
                </div>
            </div>
        </div>
        
        <div class="analysis-section">
            <div class="analysis-label">Cảm xúc thể hiện:</div>
            <div class="emotion-tags">${emotionTags}</div>
        </div>
    `;
    
    elements.roleplayAnalysis.innerHTML = html;
    elements.roleplayAnalysis.classList.remove('hidden');
}

function toggleRoleplayRecording() {
    if (!state.recognition) {
        showToast('❌', 'Trình duyệt không hỗ trợ nhận diện giọng nói');
        return;
    }
    
    if (state.isRecording) {
        stopRoleplayRecording();
    } else {
        startRoleplayRecording();
    }
}

function startRoleplayRecording() {
    state.isRecording = true;
    elements.roleplayMicBtn.classList.add('recording');
    
    state.recognition.lang = 'en-US';
    
    state.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        elements.roleplayInput.value = transcript;
        stopRoleplayRecording();
    };
    
    try {
        state.recognition.start();
        showToast('🎤', 'Đang nghe em nói tiếng Anh...');
    } catch (error) {
        console.error('Recording error:', error);
        stopRoleplayRecording();
    }
}

function stopRoleplayRecording() {
    state.isRecording = false;
    elements.roleplayMicBtn.classList.remove('recording');
    
    try {
        state.recognition.stop();
    } catch (error) {
        // Ignore
    }
}

function showCorrection() {
    if (!state.currentAnalysis || !state.currentAnalysis.practice_sentence) {
        showToast('⚠️', 'Chưa có câu nào để sửa');
        return;
    }
    
    speakText(state.currentAnalysis.practice_sentence);
    showToast('🔊', 'Nghe cách nói đúng nhé!');
}

function showNaturalSuggestion() {
    if (!state.currentAnalysis || !state.currentAnalysis.suggestions) {
        showToast('⚠️', 'Chưa có gợi ý');
        return;
    }
    
    const suggestions = state.currentAnalysis.suggestions;
    if (suggestions.length > 0) {
        showToast('💡', suggestions[0]);
    } else {
        showToast('✅', 'Câu của em đã tự nhiên rồi!');
    }
}

async function showAnswerSuggestion() {
    // Hiển thị gợi ý câu trả lời từ AI
    try {
        showToast('💡', 'Đang lấy gợi ý...');
        
        const response = await fetch('/api/roleplay/suggest');
        const data = await response.json();
        
        if (data.success && data.suggestions) {
            const suggestions = data.suggestions;
            
            // Hiển thị gợi ý trong analysis area
            const html = `
                <div class="analysis-title">💡 Gợi ý câu trả lời</div>
                
                <div class="analysis-section" style="background: #e3f2fd;">
                    <div class="analysis-label">Cách nói đơn giản:</div>
                    <div style="font-weight: 600; color: #1565c0; font-size: 1.1rem; margin: 8px 0;">
                        "${suggestions.simple}"
                    </div>
                    <button onclick="speakText('${suggestions.simple.replace(/'/g, "\\'")}')" 
                            style="padding: 6px 12px; background: #2196f3; color: white; border: none; 
                                   border-radius: 4px; cursor: pointer; font-size: 0.9rem;">
                        🔊 Nghe
                    </button>
                </div>
                
                <div class="analysis-section" style="background: #f3e5f5;">
                    <div class="analysis-label">Cách nói tự nhiên hơn:</div>
                    <div style="font-weight: 600; color: #7b1fa2; font-size: 1.1rem; margin: 8px 0;">
                        "${suggestions.natural}"
                    </div>
                    <button onclick="speakText('${suggestions.natural.replace(/'/g, "\\'")}')" 
                            style="padding: 6px 12px; background: #9c27b0; color: white; border: none; 
                                   border-radius: 4px; cursor: pointer; font-size: 0.9rem;">
                        🔊 Nghe
                    </button>
                </div>
                
                <div class="analysis-section">
                    <div style="color: #666; font-size: 0.9rem;">
                        💪 Chọn 1 câu và nói theo! Sau đó nhấn "Gửi" để tiếp tục hội thoại.
                    </div>
                </div>
            `;
            
            elements.roleplayAnalysis.innerHTML = html;
            elements.roleplayAnalysis.classList.remove('hidden');
            
            // Auto-fill vào input để user dễ sửa
            elements.roleplayInput.value = suggestions.simple;
            elements.roleplayInput.focus();
            
            showToast('✨', 'Đã có gợi ý! Em có thể sửa rồi gửi nhé.');
        } else {
            showToast('❌', 'Chưa có gợi ý, em thử tự trả lời nhé!');
        }
        
    } catch (error) {
        console.error('Get suggestion error:', error);
        showToast('❌', 'Không thể lấy gợi ý. Em thử tự trả lời nhé!');
    }
}

async function endRoleplay() {
    // Get feedback summary
    try {
        const response = await fetch('/api/roleplay/feedback');
        const data = await response.json();
        
        if (data.success) {
            const feedback = data.feedback;
            const msg = `🎉 Kết thúc luyện!\n${feedback.total_turns} lượt trò chuyện\nĐộ tự nhiên trung bình: ${feedback.average_naturalness}/5`;
            showToast('🎭', msg);
        }
    } catch (error) {
        console.error('Get feedback error:', error);
    }
    
    // Reset and close
    resetRoleplayUI();
    closeModal('roleplayModal');
}

// ==========================================
// Situation Advisor Functions
// ==========================================
function resetSituationUI() {
    // Reset UI to input state
    elements.situationInputSection.classList.remove('hidden');
    elements.situationResult.classList.add('hidden');
    elements.situationPracticeSection.classList.add('hidden');
    
    // Clear inputs
    if (elements.situationInput) {
        elements.situationInput.value = '';
    }
    if (elements.situationPracticeInput) {
        elements.situationPracticeInput.value = '';
    }
    
    // Clear analysis
    if (elements.situationAnalysis) {
        elements.situationAnalysis.innerHTML = '';
    }
    if (elements.situationPracticeFeedback) {
        elements.situationPracticeFeedback.innerHTML = '';
        elements.situationPracticeFeedback.classList.add('hidden');
    }
    
    // Reset state
    state.currentSituation = null;
    state.currentSituationAdvice = null;
}

async function analyzeSituation() {
    const situation = elements.situationInput.value.trim();
    
    if (!situation) {
        showToast('⚠️', 'Em mô tả tình huống đang gặp phải nhé!');
        return;
    }
    
    // Kiểm tra freemium limit cho guest
    if (state.isGuest) {
        const check = checkGuestLimit('situation');
        if (!check.allowed) {
            showLimitModal();
            return;
        }
        incrementGuestLimit('situation');
    }
    
    // Show loading
    showToast('⏳', 'Cô đang phân tích tình huống...');
    
    try {
        const response = await fetch('/api/situation/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ situation })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store advice
            state.currentSituationAdvice = data;
            
            // Hide input, show result
            elements.situationInputSection.classList.add('hidden');
            elements.situationResult.classList.remove('hidden');
            
            // Render analysis
            renderSituationAnalysis(data);
            
            // Auto speak simple sentence
            speakText(data.simple_en || '');
            
            showToast('✅', 'Cô đã phân tích xong! Nghe câu gợi ý nhé.');
        } else {
            showToast('❌', data.error || 'Không thể phân tích tình huống');
        }
        
    } catch (error) {
        console.error('Analyze situation error:', error);
        showToast('❌', 'Có lỗi xảy ra. Em thử lại nhé!');
    }
}

function renderSituationAnalysis(data) {
    const html = `
        <div class="analysis-block situation">
            <div class="analysis-header">🧩 TÌNH HUỐNG</div>
            <div class="analysis-content">
                <div class="vi-text">${data.situation_vn || ''}</div>
                <div class="en-text">${data.situation_en || ''}</div>
            </div>
        </div>
        
        <div class="analysis-block solution">
            <div class="analysis-header">✅ CÁCH XỬ LÝ</div>
            <div class="analysis-content">
                <div class="vi-text">${data.solution_vn || ''}</div>
                <div class="en-text">${data.solution_en || ''}</div>
            </div>
        </div>
        
        <div class="analysis-block simple">
            <div class="analysis-header">💬 CÂU ĐƠN GIẢN</div>
            <div class="analysis-content">
                <div class="en-text">"${data.simple_en || ''}"</div>
                <div class="vi-text">${data.simple_vn || ''}</div>
                <button onclick="speakText('${(data.simple_en || '').replace(/'/g, "\\'")}')" 
                        class="speak-btn-inline">
                    🔊 Nghe
                </button>
            </div>
        </div>
        
        <div class="analysis-block natural">
            <div class="analysis-header">✨ CÂU TỰ NHIÊN HƠN</div>
            <div class="analysis-content">
                <div class="en-text">"${data.natural_en || ''}"</div>
                <div class="vi-text">${data.natural_vn || ''}</div>
                <button onclick="speakText('${(data.natural_en || '').replace(/'/g, "\\'")}')" 
                        class="speak-btn-inline">
                    🔊 Nghe
                </button>
            </div>
        </div>
        
        ${data.cultural_vn || data.cultural_en ? `
        <div class="analysis-block cultural">
            <div class="analysis-header">⚠️ LƯU Ý VĂN HÓA</div>
            <div class="analysis-content">
                <div class="vi-text">${data.cultural_vn || ''}</div>
                <div class="en-text">${data.cultural_en || ''}</div>
            </div>
        </div>
        ` : ''}
        
        <div class="analysis-block practice">
            <div class="analysis-header">🔁 EM LUYỆN LẠI</div>
            <div class="analysis-content">
                <div class="vi-text">${data.practice_prompt_vn || 'Bây giờ em thử trả lời bằng tiếng Anh nhé!'}</div>
                <div class="en-text">${data.practice_prompt_en || 'Now try to respond in English!'}</div>
            </div>
        </div>
    `;
    
    elements.situationAnalysis.innerHTML = html;
}

function startSituationPractice() {
    // Hide result, show practice
    elements.situationResult.classList.add('hidden');
    elements.situationPracticeSection.classList.remove('hidden');
    
    // Set practice prompt
    const advice = state.currentSituationAdvice;
    if (advice && elements.practicePromptText) {
        elements.practicePromptText.textContent = advice.practice_prompt_vn || 'Bây giờ em thử trả lời bằng tiếng Anh nhé!';
    }
    
    // Focus input
    if (elements.situationPracticeInput) {
        elements.situationPracticeInput.focus();
    }
    
    showToast('🎤', 'Thử nói câu tiếng Anh em vừa học nhé!');
}

async function submitSituationPractice() {
    const answer = elements.situationPracticeInput.value.trim();
    
    if (!answer) {
        showToast('⚠️', 'Em nhập câu trả lời trước nhé!');
        return;
    }
    
    // Show feedback
    const advice = state.currentSituationAdvice;
    const expectedSimple = advice?.simple_en || '';
    const expectedNatural = advice?.natural_en || '';
    
    // Simple feedback
    let feedback = '';
    let isGood = false;
    
    // Check if answer contains keywords from expected sentences
    const answerLower = answer.toLowerCase();
    const expectedWords = expectedSimple.toLowerCase().split(' ');
    const matchCount = expectedWords.filter(word => 
        word.length > 2 && answerLower.includes(word)
    ).length;
    
    if (matchCount >= 2 || answerLower.includes(expectedSimple.toLowerCase().split(' ').slice(0, 3).join(' '))) {
        feedback = '🎉 Tuyệt vời! Em nói đúng ý rồi! Hãy thử nói tự nhiên hơn nhé!';
        isGood = true;
    } else {
        feedback = '💪 Gần đúng rồi! Em tham khảo lại câu gợi ý và thử lại nhé!';
    }
    
    // Display feedback
    const feedbackHtml = `
        <div style="margin-bottom: 10px; font-weight: 600; color: ${isGood ? '#27ae60' : '#f39c12'};">
            ${feedback}
        </div>
        <div style="color: #666; font-size: 0.9rem;">
            <strong>Câu của em:</strong> "${answer}"<br>
            <strong>Câu gợi ý:</strong> "${expectedSimple}"
        </div>
        <div style="margin-top: 10px;">
            <button onclick="speakText('${answer.replace(/'/g, "\\'")}')" 
                    style="padding: 5px 10px; background: var(--primary-color); color: white; 
                           border: none; border-radius: 4px; cursor: pointer; margin-right: 5px;">
                🔊 Nghe lại câu của em
            </button>
            <button onclick="resetSituationPractice()" 
                    style="padding: 5px 10px; background: #95a5a6; color: white; 
                           border: none; border-radius: 4px; cursor: pointer;">
                🔄 Thử lại
            </button>
        </div>
    `;
    
    elements.situationPracticeFeedback.innerHTML = feedbackHtml;
    elements.situationPracticeFeedback.classList.remove('hidden');
    
    // Speak the user's answer
    speakText(answer);
}

function resetSituationPractice() {
    if (elements.situationPracticeInput) {
        elements.situationPracticeInput.value = '';
    }
    if (elements.situationPracticeFeedback) {
        elements.situationPracticeFeedback.innerHTML = '';
        elements.situationPracticeFeedback.classList.add('hidden');
    }
    if (elements.situationPracticeInput) {
        elements.situationPracticeInput.focus();
    }
}

function toggleSituationPracticeRecording() {
    if (!state.recognition) {
        showToast('❌', 'Trình duyệt không hỗ trợ nhận diện giọng nói');
        return;
    }
    
    if (state.isRecording) {
        stopSituationPracticeRecording();
    } else {
        startSituationPracticeRecording();
    }
}

function startSituationPracticeRecording() {
    state.isRecording = true;
    elements.situationPracticeMicBtn.classList.add('recording');
    
    state.recognition.lang = 'en-US';
    
    state.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        elements.situationPracticeInput.value = transcript;
        stopSituationPracticeRecording();
    };
    
    try {
        state.recognition.start();
        showToast('🎤', 'Đang nghe em nói tiếng Anh...');
    } catch (error) {
        console.error('Recording error:', error);
        stopSituationPracticeRecording();
    }
}

function stopSituationPracticeRecording() {
    state.isRecording = false;
    elements.situationPracticeMicBtn.classList.remove('recording');
    
    try {
        state.recognition.stop();
    } catch (error) {
        // Ignore
    }
}

// ==========================================
// User Authentication Functions
// ==========================================
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    
    // Detect if email or phone
    const isEmail = email.includes('@');
    const loginData = isEmail ? { email, password } : { phone: email, password };
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(loginData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            state.currentUser = data.user;
            state.isGuest = false;
            updateAuthUI();
            updateUserBadge();
            closeModal('loginModal');
            showToast('✅', `Chào mừng ${data.user.name}!`);
        } else {
            showToast('❌', data.error || 'Đăng nhập thất bại');
        }
    } catch (error) {
        console.error('Login error:', error);
        showToast('❌', 'Có lỗi xảy ra, thử lại nhé!');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const email = document.getElementById('regEmail').value.trim();
    const phone = document.getElementById('regPhone').value.trim();
    const name = document.getElementById('regName').value.trim();
    const password = document.getElementById('regPassword').value;
    
    try {
        const referral_code = state.referralCode || null;
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, phone, name, password, referral_code })
        });
        
        const data = await response.json();
        
        if (data.success) {
            state.pendingUserId = data.user.id;
            closeModal('registerModal');
            openModal('profileSetupModal');
            showToast('🎉', 'Đăng ký thành công! Hoàn thiện hồ sơ nhé.');
        } else {
            showToast('❌', data.error || 'Đăng ký thất bại');
        }
    } catch (error) {
        console.error('Register error:', error);
        showToast('❌', 'Có lỗi xảy ra, thử lại nhé!');
    }
}

async function handleProfileSetup(e) {
    e.preventDefault();
    
    if (!state.pendingUserId) {
        showToast('❌', 'Không tìm thấy thông tin đăng ký');
        return;
    }
    
    const form = e.currentTarget;
    const profile = {
        age: form.querySelector('#profileAge').value,
        job: form.querySelector('#profileJob').value,
        meet_foreigners: form.querySelector('input[name="meetForeigners"]:checked').value === 'true',
        english_usage: form.querySelector('#profileUsage').value,
        goal: form.querySelector('#profileGoal').value,
        level: form.querySelector('#profileLevel').value,
        learning_path: form.querySelector('#profileLearningPath')?.value || 'communication',
        grade_level: form.querySelector('#profileGradeLevel')?.value || ''
    };
    
    try {
        const response = await fetch('/api/auth/profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: state.pendingUserId, profile })
        });
        
        const data = await response.json();
        
        if (data.success) {
            state.currentUser = data.user;
            state.pendingUserId = null;
            updateAuthUI();
            closeModal('profileSetupModal');
            showToast('🎉', `Hoàn tất! Chào mừng ${data.user.name}!`);
        } else {
            showToast('❌', data.error || 'Cập nhật thất bại');
        }
    } catch (error) {
        console.error('Profile setup error:', error);
        showToast('❌', 'Có lỗi xảy ra, thử lại nhé!');
    }
}

async function logout() {
    try {
        await fetch('/api/auth/logout', { method: 'POST' });
    } catch (error) {
        console.error('Logout error:', error);
    }
    
    state.currentUser = null;
    state.pendingUserId = null;
    state.isGuest = true;
    updateAuthUI();
    updateUserBadge();
    loadGuestLimits(); // Reset guest limits
    showToast('👋', 'Đã đăng xuất. Hẹn gặp lại!');
}

function updateAuthUI() {
    const isLoggedIn = !!state.currentUser;
    const isAdmin = state.currentUser?.role === 'admin';
    
    // Toggle buttons
    if (elements.loginBtn) elements.loginBtn.classList.toggle('hidden', isLoggedIn);
    if (elements.registerBtn) elements.registerBtn.classList.toggle('hidden', isLoggedIn);
    if (elements.logoutBtn) elements.logoutBtn.classList.toggle('hidden', !isLoggedIn);
    if (elements.dashboardBtn) elements.dashboardBtn.classList.toggle('hidden', !isLoggedIn);
    if (elements.profileBtn) elements.profileBtn.classList.toggle('hidden', !isLoggedIn);
    if (elements.feedbackBtn) elements.feedbackBtn.classList.toggle('hidden', !isLoggedIn);
    if (elements.affiliateBtn) elements.affiliateBtn.classList.toggle('hidden', !isLoggedIn);
    if (elements.adminBtn) elements.adminBtn.classList.toggle('hidden', !isAdmin);
}

// ==========================================
// Dashboard Functions
// ==========================================
async function showDashboard() {
    if (!state.currentUser) {
        showToast('⚠️', 'Vui lòng đăng nhập để xem tiến độ');
        openModal('loginModal');
        return;
    }
    
    try {
        const [progressRes, roadmapRes] = await Promise.all([
            fetch(`/api/user/progress?user_id=${state.currentUser.id}`),
            fetch(`/api/roadmap/dashboard?user_id=${state.currentUser.id}`)
        ]);
        const data = await progressRes.json();
        const roadmapData = await roadmapRes.json();
        
        if (data.success) {
            data.roadmapDashboard = roadmapData.success ? roadmapData.dashboard : {};
            renderDashboard(data);
            openModal('dashboardModal');
        } else {
            showToast('❌', data.error || 'Không thể tải tiến độ');
        }
    } catch (error) {
        console.error('Dashboard error:', error);
        showToast('❌', 'Có lỗi xảy ra, thử lại nhé!');
    }
}

function renderDashboard(data) {
    const progress = data.progress || {};
    const roadmap = data.roadmapDashboard || {};
    const errors = data.common_errors || [];
    const situations = progress.practiced_situations || [];
    if (elements.dashboardContent) {
        const existing = document.getElementById('learningProfileSummary');
        if (!existing) {
            elements.dashboardContent.insertAdjacentHTML('afterbegin', '<div id="learningProfileSummary" class="learning-profile-summary"></div>');
        }
        const summary = document.getElementById('learningProfileSummary');
        if (summary) {
            summary.innerHTML = `
                <div class="profile-level-card">
                    <span>Current level</span>
                    <strong>${escapeHtml(roadmap.currentLevel || 'starter')}</strong>
                </div>
                <div class="profile-metric"><strong>${roadmap.totalXP || progress.total_xp || 0}</strong><span>XP</span></div>
                <div class="profile-metric"><strong>${roadmap.completedLessons || progress.completed_lessons || 0}</strong><span>Lessons</span></div>
                <div class="profile-metric"><strong>${roadmap.speakingPractices || progress.speaking_practices || 0}</strong><span>Speaking</span></div>
                <div class="profile-metric"><strong>${roadmap.pronunciationScoreAvg || progress.avg_natural_score || 0}</strong><span>Pronunciation</span></div>
                <div class="profile-badges">${(roadmap.badges || progress.badges || []).slice(-5).map(b => `<span><i class="fas fa-award"></i> ${escapeHtml(b.title)}</span>`).join('') || '<span>No badges yet</span>'}</div>
            `;
        }
    }
    
    // Update streak
    const streakEl = document.getElementById('dashboardStreak');
    const longestStreakEl = document.getElementById('longestStreak');
    if (streakEl) streakEl.textContent = progress.current_streak || 0;
    if (longestStreakEl) longestStreakEl.textContent = progress.longest_streak || 0;
    
    // Update stats
    const dashTotalDays = document.getElementById('dashTotalDays');
    const dashSentences = document.getElementById('dashSentences');
    const dashSituations = document.getElementById('dashSituations');
    
    if (dashTotalDays) dashTotalDays.textContent = progress.total_days_studied || 0;
    if (dashSentences) dashSentences.textContent = progress.total_sentences_practiced || 0;
    if (dashSituations) dashSituations.textContent = progress.total_situations_practiced || 0;
    
    // Update scores
    const grammarScore = progress.avg_grammar_score || 0;
    const naturalScore = progress.avg_natural_score || 0;
    
    const grammarScoreBar = document.getElementById('grammarScoreBar');
    const grammarScoreVal = document.getElementById('grammarScore');
    const naturalScoreBar = document.getElementById('naturalScoreBar');
    const naturalScoreVal = document.getElementById('naturalScore');
    
    if (grammarScoreBar) grammarScoreBar.style.width = `${grammarScore}%`;
    if (grammarScoreVal) grammarScoreVal.textContent = `${Math.round(grammarScore)}/100`;
    if (naturalScoreBar) naturalScoreBar.style.width = `${naturalScore}%`;
    if (naturalScoreVal) naturalScoreVal.textContent = `${Math.round(naturalScore)}/100`;
    
    // Update common errors
    const errorsList = document.getElementById('commonErrorsList');
    if (errorsList) {
        if (errors.length === 0) {
            errorsList.innerHTML = '<p class="empty-text">Tuyệt vời! Bạn chưa có lỗi nào được ghi nhận.</p>';
        } else {
            errorsList.innerHTML = errors.map(e => `
                <div class="error-item">
                    <span class="error-text">${e.error_type}</span>
                    <span class="error-count">${e.count}x</span>
                </div>
            `).join('');
        }
    }
    
    // Update practiced situations
    const situationsList = document.getElementById('practicedSituationsList');
    if (situationsList) {
        if (situations.length === 0) {
            situationsList.innerHTML = '<p class="empty-text">Hãy luyện tập tình huống đầu tiên!</p>';
        } else {
            situationsList.innerHTML = situations.slice(-5).reverse().map(s => `
                <div class="situation-item">
                    <span>${s.situation || s}</span>
                    <span class="situation-date">${s.date || ''}</span>
                </div>
            `).join('');
        }
    }
}

// ==========================================
// Progress Tracking Helper
// ==========================================
async function recordUserActivity(type, content, scores = {}, errors = []) {
    if (!state.currentUser) return;
    
    try {
        await fetch('/api/user/activity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: state.currentUser.id,
                type,
                content,
                grammar_score: scores.grammar,
                natural_score: scores.natural,
                errors
            })
        });
    } catch (error) {
        console.error('Record activity error:', error);
    }
}

async function updateUserProgress(sessionData) {
    if (!state.currentUser) return;
    
    try {
        await fetch('/api/user/progress', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: state.currentUser.id,
                session: sessionData
            })
        });
    } catch (error) {
        console.error('Update progress error:', error);
    }
}

// ==========================================
// Keyboard Shortcuts
// ==========================================
document.addEventListener('keydown', (e) => {
    // ESC to close modals
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal').forEach(modal => {
            if (!modal.classList.contains('hidden')) {
                closeModal(modal.id);
            }
        });
    }
});

// ==========================================
// Enhanced TTS (Text-to-Speech)
// ==========================================
function initializeTTS() {
    if (!('speechSynthesis' in window)) {
        console.log('Browser không hỗ trợ TTS');
        return;
    }
    
    // Load voices
    loadVoices();
    
    // Voices might load asynchronously
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = loadVoices;
    }
}

let englishVoices = [];

// ==========================================
// Freemium Functions
// ==========================================
const FREEMIUM_LIMITS = {
    chat: 5,
    situation: 1,
    roleplay: 1
};

function loadGuestLimits() {
    const today = new Date().toDateString();
    const saved = localStorage.getItem('ms_smile_guest_limits');
    
    if (saved) {
        const data = JSON.parse(saved);
        if (data.lastReset === today) {
            state.guestLimits = data;
            return;
        }
    }
    
    // Reset nếu qua ngày mới
    state.guestLimits = {
        chat: 0,
        situation: 0,
        roleplay: 0,
        lastReset: today
    };
    saveGuestLimits();
}

function saveGuestLimits() {
    localStorage.setItem('ms_smile_guest_limits', JSON.stringify(state.guestLimits));
}

function checkGuestLimit(type) {
    // Nếu đã đăng nhập, không giới hạn
    if (!state.isGuest && state.currentUser) {
        return { allowed: true, remaining: Infinity };
    }
    
    // Kiểm tra và reset nếu qua ngày mới
    const today = new Date().toDateString();
    if (state.guestLimits.lastReset !== today) {
        state.guestLimits = {
            chat: 0,
            situation: 0,
            roleplay: 0,
            lastReset: today
        };
        saveGuestLimits();
    }
    
    const current = state.guestLimits[type] || 0;
    const limit = FREEMIUM_LIMITS[type];
    const remaining = limit - current;
    
    return {
        allowed: remaining > 0,
        remaining: remaining,
        used: current,
        limit: limit
    };
}

function incrementGuestLimit(type) {
    if (!state.isGuest && state.currentUser) return true;
    
    const check = checkGuestLimit(type);
    if (!check.allowed) {
        showLimitModal();
        return false;
    }
    
    state.guestLimits[type]++;
    saveGuestLimits();
    return true;
}

function showLimitModal() {
    const check = {
        chat: checkGuestLimit('chat'),
        situation: checkGuestLimit('situation'),
        roleplay: checkGuestLimit('roleplay')
    };
    
    // Update display
    if (elements.chatLimitDisplay) {
        elements.chatLimitDisplay.textContent = `${check.chat.used}/${check.chat.limit}`;
    }
    if (elements.situationLimitDisplay) {
        elements.situationLimitDisplay.textContent = `${check.situation.used}/${check.situation.limit}`;
    }
    if (elements.roleplayLimitDisplay) {
        elements.roleplayLimitDisplay.textContent = `${check.roleplay.used}/${check.roleplay.limit}`;
    }
    
    // Show modal
    if (elements.limitModal) {
        elements.limitModal.classList.remove('hidden');
    }
}

function updateUserBadge() {
    if (!elements.userBadge || !elements.userBadgeText) return;
    
    if (state.currentUser) {
        // Đã đăng nhập
        elements.userBadge.classList.remove('guest-badge');
        elements.userBadge.classList.add('user-badge');
        elements.userBadgeText.textContent = state.currentUser.name || 'User';
        if (elements.dashboardBtn) elements.dashboardBtn.classList.remove('hidden');
        if (elements.profileBtn) elements.profileBtn.classList.remove('hidden');
        if (elements.logoutBtn) elements.logoutBtn.classList.remove('hidden');
        if (elements.loginBtn) elements.loginBtn.classList.add('hidden');
        if (elements.registerBtn) elements.registerBtn.classList.add('hidden');
        if (elements.adminBtn) {
            if (state.currentUser.role === 'admin') {
                elements.adminBtn.classList.remove('hidden');
            } else {
                elements.adminBtn.classList.add('hidden');
            }
        }
    } else {
        // Khách
        elements.userBadge.classList.remove('user-badge');
        elements.userBadge.classList.add('guest-badge');
        elements.userBadgeText.textContent = 'Khách dùng thử';
        if (elements.dashboardBtn) elements.dashboardBtn.classList.add('hidden');
        if (elements.profileBtn) elements.profileBtn.classList.add('hidden');
        if (elements.logoutBtn) elements.logoutBtn.classList.add('hidden');
        if (elements.loginBtn) elements.loginBtn.classList.remove('hidden');
        if (elements.registerBtn) elements.registerBtn.classList.remove('hidden');
        if (elements.adminBtn) elements.adminBtn.classList.add('hidden');
    }
}

function loadVoices() {
    if (!('speechSynthesis' in window)) {
        englishVoices = [];
        return;
    }

    const voices = speechSynthesis.getVoices();
    englishVoices = voices.filter(v => v.lang.startsWith('en'));
    console.log('[TTS] English voices loaded:', englishVoices.length, englishVoices.map(v => v.name));
}



function escapeAttr(value) {
    return String(value || '')
        .replace(/&/g, '&amp;')
        .replace(/"/g, '&quot;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function playDailyLessonAudio(text, button = null) {
    console.log('[DailyLessonAudio] playDailyLessonAudio called');
    console.log('[DailyLessonAudio] text:', text ? text.substring(0, 50) : 'null');
    console.log('[DailyLessonAudio] typeof text:', typeof text);
    
    if (!text || !text.trim()) {
        console.warn('[DailyLessonAudio] empty text, skipping');
        return;
    }
    
    console.log('[DailyLessonAudio] calling speakText');
    speakText(text, null, button);
    console.log('[DailyLessonAudio] speakText called');
}

function speakText(text, rate = null, sourceButton = null) {
    console.log('[TTS] speakText called with text:', text ? text.substring(0, 50) : 'null');
    
    if (!('speechSynthesis' in window)) {
        console.error('[TTS] speechSynthesis not supported');
        showToast('❌', 'Trình duyệt không hỗ trợ đọc văn bản');
        return;
    }
    
    const cleanText = String(text || '').trim();
    if (!cleanText) {
        return;
    }

    if (englishVoices.length === 0) {
        loadVoices();
    }

    // Cancel any ongoing speech
    console.log('[TTS] Cancelling previous speech');
    speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(cleanText);
    
    // Set voice to English if available
    if (englishVoices.length > 0) {
        // Prefer US English, then any English
        const usVoice = englishVoices.find(v => v.lang === 'en-US');
        utterance.voice = usVoice || englishVoices[0];
        utterance.lang = utterance.voice.lang || 'en-US';
        console.log('[TTS] Using voice:', utterance.voice?.name, utterance.voice?.lang);
    } else {
        console.warn('[TTS] No English voices available');
        utterance.lang = 'en-US';
    }
    
    // Set rate (speed)
    utterance.rate = rate || state.ttsSpeed || 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    
    console.log('[TTS] volume/rate/pitch:', utterance.volume, utterance.rate, utterance.pitch);
    console.log('[TTS] text length:', text.length);
    
    utterance.onstart = () => {
        state.isSpeaking = true;
        if (sourceButton) sourceButton.classList.add('speaking');
        console.log('[TTS] onstart', text.substring(0, 30));
    };
    
    utterance.onend = () => {
        state.isSpeaking = false;
        if (sourceButton) sourceButton.classList.remove('speaking');
        console.log('[TTS] onend', text.substring(0, 30));
    };
    
    utterance.onerror = (e) => {
        console.error('[TTS] onerror', e.error, e.message || '');
        state.isSpeaking = false;
        if (sourceButton) sourceButton.classList.remove('speaking');
        if (e.error !== 'interrupted' && e.error !== 'canceled') {
            showToast('❌', 'Chưa phát được âm thanh. Em thử bấm lại một lần nhé.');
        }
    };
    
    console.log('[TTS] Calling synthesis.speak()');
    speechSynthesis.speak(utterance);

    // Some Android browsers leave synthesis paused after a previous cancel.
    if (speechSynthesis.paused) {
        speechSynthesis.resume();
    }

    setTimeout(() => {
        if (speechSynthesis.paused) {
            speechSynthesis.resume();
        }
    }, 100);

    console.log('[TTS] speak() called');
}

window.speakText = speakText;

function stopSpeaking() {
    if ('speechSynthesis' in window) {
        speechSynthesis.cancel();
        state.isSpeaking = false;
    }
}

// Add speak button to AI messages
function addSpeakButtonToMessage(messageContent, text) {
    const speakBtn = document.createElement('button');
    speakBtn.className = 'speak-btn';
    speakBtn.innerHTML = '🔊';
    speakBtn.title = 'Nghe cô đọc';
    speakBtn.onclick = () => {
        if (state.isSpeaking) {
            stopSpeaking();
            speakBtn.classList.remove('speaking');
        } else {
            speakText(text);
            speakBtn.classList.add('speaking');
            setTimeout(() => speakBtn.classList.remove('speaking'), 5000);
        }
    };
    messageContent.appendChild(speakBtn);
}

// ==========================================
// Enhanced Speech Recognition
// ==========================================
function startRecordingWithFeedback() {
    if (!state.recognition) {
        showToast('❌', 'Trình duyệt không hỗ trợ nhận diện giọng nói');
        return;
    }
    
    state.isRecording = true;
    elements.micBtn.classList.add('recording');
    elements.recordingIndicator.classList.remove('hidden');
    
    // Detect language automatically
    const isVietnamese = /[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]/i.test(elements.messageInput.value);
    state.recognition.lang = isVietnamese ? 'vi-VN' : 'en-US';
    
    try {
        state.recognition.start();
        showToast('🎤', 'Đang nghe... Em nói đi!');
    } catch (error) {
        console.error('Recording error:', error);
        stopRecording();
    }
}

// ==========================================
// Basic Pronunciation Feedback
// ==========================================
function getBasicPronunciationFeedback(spoken, expected) {
    const spokenWords = spoken.toLowerCase().trim().split(/\s+/);
    const expectedWords = expected.toLowerCase().trim().split(/\s+/);
    
    const feedback = {
        missing: [],
        wrong: [],
        extra: [],
        correct: [],
        score: 0
    };
    
    // Simple word-by-word comparison
    let spokenIndex = 0;
    let expectedIndex = 0;
    
    while (expectedIndex < expectedWords.length || spokenIndex < spokenWords.length) {
        const expectedWord = expectedWords[expectedIndex];
        const spokenWord = spokenWords[spokenIndex];
        
        if (!spokenWord && expectedWord) {
            feedback.missing.push(expectedWord);
            expectedIndex++;
        } else if (spokenWord && !expectedWord) {
            feedback.extra.push(spokenWord);
            spokenIndex++;
        } else if (spokenWord === expectedWord) {
            feedback.correct.push(spokenWord);
            spokenIndex++;
            expectedIndex++;
        } else {
            // Words don't match - try to find closest
            const similarity = calculateSimilarity(spokenWord, expectedWord);
            if (similarity > 0.6) {
                feedback.wrong.push({
                    expected: expectedWord,
                    spoken: spokenWord,
                    similarity: similarity
                });
            } else {
                feedback.missing.push(expectedWord);
                feedback.extra.push(spokenWord);
            }
            spokenIndex++;
            expectedIndex++;
        }
    }
    
    // Calculate simple score
    const totalWords = expectedWords.length;
    const correctCount = feedback.correct.length;
    feedback.score = Math.round((correctCount / totalWords) * 100);
    
    return feedback;
}

function calculateSimilarity(str1, str2) {
    // Simple Levenshtein-based similarity
    const len1 = str1.length;
    const len2 = str2.length;
    const matrix = [];
    
    for (let i = 0; i <= len1; i++) {
        matrix[i] = [i];
    }
    for (let j = 0; j <= len2; j++) {
        matrix[0][j] = j;
    }
    
    for (let i = 1; i <= len1; i++) {
        for (let j = 1; j <= len2; j++) {
            const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
            matrix[i][j] = Math.min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost
            );
        }
    }
    
    const distance = matrix[len1][len2];
    const maxLen = Math.max(len1, len2);
    return 1 - (distance / maxLen);
}

function renderBasicPronunciationFeedback(feedback, expected) {
    let html = '<div class="pronunciation-feedback">';
    html += '<div class="feedback-title">📊 Kết quả phát âm</div>';
    
    // Score
    const scoreColor = feedback.score >= 80 ? '#2ecc71' : feedback.score >= 50 ? '#f39c12' : '#e74c3c';
    html += `<div style="font-size: 2rem; font-weight: bold; color: ${scoreColor}; margin-bottom: 10px;">${feedback.score}%</div>`;
    
    // Missing words
    if (feedback.missing.length > 0) {
        html += `<div class="feedback-item missing">❌ Thiếu từ: ${feedback.missing.join(', ')}</div>`;
    }
    
    // Wrong words
    if (feedback.wrong.length > 0) {
        feedback.wrong.forEach(w => {
            html += `<div class="feedback-item">⚠️ "${w.spoken}" → nên là "${w.expected}"</div>`;
        });
    }
    
    // Extra words
    if (feedback.extra.length > 0) {
        html += `<div class="feedback-item" style="color: #3498db;">💡 Thừa từ: ${feedback.extra.join(', ')}</div>`;
    }
    
    // Encouragement
    if (feedback.score >= 80) {
        html += '<div class="feedback-item correct">🎉 Tuyệt vời! Em phát âm rất tốt!</div>';
    } else if (feedback.score >= 50) {
        html += '<div class="feedback-item suggestion">💪 Khá tốt! Cố gắng thêm một chút nhé!</div>';
    } else {
        html += '<div class="feedback-item suggestion">📚 Em thử nghe và đọc theo cô nhiều lần nhé!</div>';
    }
    
    html += '</div>';
    return html;
}

// ==========================================
// Plan Management Functions
// ==========================================
async function loadCurrentPlanInfo() {
    if (!state.currentUser) return;
    
    try {
        const response = await fetch('/api/auth/me');
        const data = await response.json();
        
        if (data.success) {
            const user = data.user;
            const planInfo = document.getElementById('currentPlanInfo');
            
            if (planInfo) {
                let html = `
                    <div style="margin-bottom: 10px;">
                        <strong>Gói hiện tại:</strong> ${user.plan_name || 'free_trial'}
                    </div>
                `;
                
                if (user.subscription_end) {
                    const endDate = new Date(user.subscription_end);
                    const now = new Date();
                    const daysLeft = Math.ceil((endDate - now) / (1000 * 60 * 60 * 24));
                    
                    html += `
                        <div style="margin-bottom: 10px;">
                            <strong>Hết hạn:</strong> ${endDate.toLocaleDateString('vi-VN')}
                            ${daysLeft > 0 ? `(${daysLeft} ngày còn lại)` : '(đã hết hạn)'}
                        </div>
                    `;
                }
                
                planInfo.innerHTML = html;
            }
        }
    } catch (error) {
        console.error('Error loading plan info:', error);
    }
}

async function loadPlanOptions() {
    try {
        const response = await fetch('/api/plans');
        const data = await response.json();
        if (!data.success) return;

        const planOptions = document.getElementById('planOptions');
        if (!planOptions) return;

        const plans = data.plans
            .filter(plan => plan.enabled && plan.name !== 'free_trial')
            .sort((a, b) => (a.price || 0) - (b.price || 0));
        const paymentInfo = data.payment_info || {};

        planOptions.innerHTML = renderPlanCheckout(plans, paymentInfo);
        setupPlanCheckoutEvents(plans, paymentInfo);
    } catch (error) {
        console.error('Error loading plans:', error);
        showToast('?', 'Khong the tai danh sach goi');
    }
}

function renderPlanCheckout(plans, paymentInfo) {
    if (!plans.length) {
        return '<p>Chua co goi dich vu dang mo ban.</p>';
    }

    const planOptions = plans.map(plan => `
        <option value="${plan.name}">${escapeHtml(plan.title)} - ${formatMoneyVnd(plan.price)} VND</option>
    `).join('');

    return `
        <div class="plan-checkout">
            <div class="plan-checkout-grid">
                <div class="plan-picker">
                    <h3>Chon goi dang ky</h3>
                    <div class="form-group">
                        <label>Goi dich vu</label>
                        <select id="planSelect">${planOptions}</select>
                    </div>
                    <div id="selectedPlanDetail" class="selected-plan-detail"></div>
                    <button id="createPaymentRequestBtn" class="btn btn-primary btn-block">Tao yeu cau thanh toan</button>
                    ${state.currentUser ? '' : '<p class="payment-hint">Ban can dang nhap hoac dang ky truoc khi tao yeu cau thanh toan.</p>'}
                </div>
                <div class="payment-info-card">
                    <h3>Thong tin chuyen khoan</h3>
                    <div><strong>Ngan hang:</strong> ${escapeHtml(paymentInfo.bank_name || 'Chua cau hinh')}</div>
                    <div><strong>Chu tai khoan:</strong> ${escapeHtml(paymentInfo.account_name || 'Chua cau hinh')}</div>
                    <div><strong>So tai khoan:</strong> ${escapeHtml(paymentInfo.account_number || 'Chua cau hinh')}</div>
                    <div><strong>So dien thoai admin:</strong> ${escapeHtml(paymentInfo.admin_phone || 'Chua cau hinh')}</div>
                    <p>${escapeHtml(paymentInfo.support_note || '')}</p>
                    <div id="paymentResult" class="payment-result hidden"></div>
                </div>
            </div>
        </div>
    `;
}

function setupPlanCheckoutEvents(plans, paymentInfo) {
    const select = document.getElementById('planSelect');
    const createBtn = document.getElementById('createPaymentRequestBtn');
    const detail = document.getElementById('selectedPlanDetail');
    if (!select || !createBtn || !detail) return;

    const renderSelected = () => {
        const plan = plans.find(item => item.name === select.value) || plans[0];
        if (!plan) return;
        detail.innerHTML = `
            <div><strong>${escapeHtml(plan.title)}</strong></div>
            <div class="plan-price">${formatMoneyVnd(plan.price)} VND</div>
            <div>Thoi han: ${plan.duration_days || 30} ngay</div>
            <div>Chat: ${plan.chat_per_day || plan.chat_limit || 0}/ngay</div>
            <div>Bai hoc: ${plan.lesson_limit || 0}/ngay</div>
            <div>${escapeHtml(plan.description || '')}</div>
        `;
    };

    select.addEventListener('change', renderSelected);
    createBtn.addEventListener('click', () => selectPlan(select.value, paymentInfo));
    renderSelected();
}

function formatMoneyVnd(value) {
    return Number(value || 0).toLocaleString('vi-VN');
}

function escapeHtml(value) {
    return String(value || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

async function selectPlan(planName, paymentInfo = {}) {
    if (!state.currentUser) {
        showToast('?', 'Vui long dang nhap hoac dang ky truoc');
        closeModal('planModal');
        openModal('loginModal');
        return;
    }

    try {
        const response = await fetch('/api/payment/request', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: state.currentUser.id,
                plan_name: planName
            })
        });

        const data = await response.json();
        if (!data.success) {
            showToast('?', data.error || 'Khong the tao yeu cau thanh toan');
            return;
        }

        const payment = data.payment_request;
        const info = data.payment_info || paymentInfo;
        const result = document.getElementById('paymentResult');
        if (result) {
            result.classList.remove('hidden');
            result.innerHTML = `
                <h4>Yeu cau thanh toan da tao</h4>
                <div><strong>Ma yeu cau:</strong> ${escapeHtml(payment.reference_code)}</div>
                <div><strong>So tien:</strong> ${formatMoneyVnd(payment.amount)} ${escapeHtml(payment.currency)}</div>
                <div><strong>Noi dung chuyen khoan:</strong> <code>${escapeHtml(payment.transfer_note)}</code></div>
                <div><strong>Ngan hang:</strong> ${escapeHtml(info.bank_name || 'Chua cau hinh')}</div>
                <div><strong>Chu tai khoan:</strong> ${escapeHtml(info.account_name || 'Chua cau hinh')}</div>
                <div><strong>So tai khoan:</strong> ${escapeHtml(info.account_number || 'Chua cau hinh')}</div>
                <div><strong>So dien thoai admin:</strong> ${escapeHtml(info.admin_phone || 'Chua cau hinh')}</div>
                <button class="btn btn-success btn-block payment-confirm-btn" onclick="confirmPaymentPaid(${payment.id})">
                    <i class="fas fa-check-circle"></i> Da thanh toan
                </button>
                <p>Sau khi chuyen khoan xong, bam nut <strong>Da thanh toan</strong> de bao admin kiem tra va mo goi.</p>
                <div id="paymentConfirmStatus" class="payment-hint"></div>
            `;
            result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
        showToast('?', 'Da tao yeu cau thanh toan. Vui long chuyen khoan dung noi dung hien tren man hinh.');
    } catch (error) {
        console.error('Error creating payment request:', error);
        showToast('?', 'Loi ket noi server khi tao yeu cau thanh toan');
    }
}

async function confirmPaymentPaid(paymentId) {
    if (!state.currentUser) {
        openModal('loginModal');
        return;
    }
    const statusEl = document.getElementById('paymentConfirmStatus');
    if (statusEl) statusEl.textContent = 'Dang gui xac nhan...';
    try {
        const response = await fetch(`/api/payment/request/${paymentId}/confirm-paid`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: state.currentUser.id })
        });
        const data = await response.json();
        if (!data.success) {
            if (statusEl) statusEl.textContent = data.error || 'Khong xac nhan duoc.';
            showToast('?', data.error || 'Khong xac nhan duoc thanh toan');
            return;
        }
        if (statusEl) statusEl.textContent = 'Da gui cho admin. Vui long cho admin duyet mo goi.';
        showToast('?', 'Da bao admin ban da thanh toan.');
    } catch (error) {
        console.error('Confirm payment error:', error);
        if (statusEl) statusEl.textContent = 'Loi ket noi server.';
    }
}
