/**
 * Ms. Smile English - Main JavaScript Application
 * Xử lý tất cả chức năng frontend
 */

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
    statsBtn: document.getElementById('statsBtn'),
    startLessonBtn: document.getElementById('startLessonBtn'),
    profileBtn: document.getElementById('profileBtn'),
    feedbackBtn: document.getElementById('feedbackBtn'),
    
    // Modals
    lessonModal: document.getElementById('lessonModal'),
    statsModal: document.getElementById('statsModal'),
    speakingModal: document.getElementById('speakingModal'),
    onboardingModal: document.getElementById('onboardingModal'),
    profileModal: document.getElementById('profileModal'),
    feedbackModal: document.getElementById('feedbackModal'),
    
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
    plansBtn: document.getElementById('plansBtn'),
    adminBtn: document.getElementById('adminBtn'),
    dashboardModal: document.getElementById('dashboardModal'),
    dashboardContent: document.getElementById('dashboardContent'),
    plansModal: document.getElementById('plansModal'),
    plansContent: document.getElementById('plansContent'),
    affiliateModal: document.getElementById('affiliateModal'),
    affiliateCode: document.getElementById('affiliateCode'),
    affiliateLink: document.getElementById('affiliateLink'),
    copyAffiliateLinkBtn: document.getElementById('copyAffiliateLinkBtn'),
    affiliateReferredCount: document.getElementById('affiliateReferredCount'),
    affiliatePaidCount: document.getElementById('affiliatePaidCount'),
    affiliatePending: document.getElementById('affiliatePending'),
    affiliatePaid: document.getElementById('affiliatePaid'),
    familySection: document.getElementById('familySection'),
    familySummary: document.getElementById('familySummary'),
    familyMembersList: document.getElementById('familyMembersList'),
    familyMemberIdentifier: document.getElementById('familyMemberIdentifier'),
    addFamilyMemberBtn: document.getElementById('addFamilyMemberBtn'),
    
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

async function initializeApp() {
    captureReferralCode();
    setupEventListeners();
    initializeSpeechRecognition();
    initializeTTS();
    
    // Load freemium limits and update badge
    loadGuestLimits();
    updateUserBadge();
    await loadInitialData();
    await checkOnboarding();
    
    console.log('🌟 Ms. Smile English đã sẵn sàng!');
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

function formatMoney(value) {
    return Number(value || 0).toLocaleString('vi-VN');
}

async function openPlansModal() {
    await loadPlansForUser();
    openModal('plansModal');
}

async function loadPlansForUser() {
    if (!elements.plansContent) return;
    elements.plansContent.innerHTML = '<p class="empty-text">Dang tai goi dich vu...</p>';
    try {
        const response = await fetch('/api/plans');
        const data = await response.json();
        if (!data.success) {
            elements.plansContent.innerHTML = '<p class="empty-text">Khong tai duoc goi dich vu.</p>';
            return;
        }
        elements.plansContent.innerHTML = data.plans.map(plan => `
            <div class="dashboard-section">
                <h3>${plan.title || plan.name}</h3>
                <p><strong>${formatMoney(plan.price)} VND/thang</strong></p>
                <p>Chat: ${plan.chat_per_day || plan.chat_limit}/ngay - Bai hoc: ${plan.lesson_limit}/ngay</p>
                <p>Luyen phat am: ${plan.can_speak ? 'Co' : 'Khong'} - Luu lich su: ${plan.can_save_history ? 'Co' : 'Khong'}</p>
                ${plan.name === 'family' ? `<p>Family: toi da ${plan.family_member_limit || 5} users tinh ca chu goi</p>` : ''}
                ${plan.price > 0 ? `<button class="btn btn-primary btn-full" type="button" onclick="requestPlanPayment('${plan.name}')">Dang ky goi nay</button>` : ''}
            </div>
        `).join('');
    } catch (error) {
        console.error('Plans load error:', error);
        elements.plansContent.innerHTML = '<p class="empty-text">Loi tai goi dich vu.</p>';
    }
}

async function requestPlanPayment(planName) {
    if (!state.currentUser) {
        closeModal('plansModal');
        openModal('loginModal');
        showToast('⚠️', 'Dang nhap truoc khi dang ky goi');
        return;
    }
    try {
        const response = await fetch('/api/payment/request', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: state.currentUser.id, plan_name: planName })
        });
        const data = await response.json();
        if (data.success) {
            const payment = data.payment_request;
            showToast('✅', `Da tao yeu cau thanh toan: ${payment.transfer_note || payment.reference_code}`);
            alert(`Thong tin chuyen khoan\\nChu tai khoan: Nguyen Quoc Tuan\\nNoi dung: ${payment.transfer_note || payment.reference_code}\\nSo tien: ${formatMoney(payment.amount)} VND`);
        } else {
            showToast('❌', data.error || 'Khong tao duoc thanh toan');
        }
    } catch (error) {
        console.error('Payment request error:', error);
        showToast('❌', 'Loi tao yeu cau thanh toan');
    }
}

async function loadFamilyMembers() {
    if (!elements.familySection || !state.currentUser) return;
    const isFamilyOwner = state.currentUser.plan_name === 'family' && state.currentUser.status === 'active';
    elements.familySection.classList.toggle('hidden', !isFamilyOwner);
    if (!isFamilyOwner) return;

    try {
        const response = await fetch('/api/user/family/members');
        const data = await response.json();
        if (!data.success) {
            elements.familySummary.textContent = data.error || 'Khong tai duoc thanh vien Family';
            return;
        }

        const used = (data.member_count || 0) + 1;
        elements.familySummary.textContent = `Dang dung ${used}/${data.limit} users tinh ca chu goi.`;
        if (!data.members || data.members.length === 0) {
            elements.familyMembersList.innerHTML = '<p class="empty-text">Chua co thanh vien nao.</p>';
            return;
        }

        elements.familyMembersList.innerHTML = data.members.map(member => `
            <div class="error-item">
                <span class="error-text">#${member.member_user_id} ${member.member_name || ''} ${member.member_email || member.member_phone || ''}</span>
                <button type="button" class="btn btn-sm btn-secondary" onclick="removeFamilyMember(${member.id})">Xoa</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Family load error:', error);
        elements.familySummary.textContent = 'Loi tai thanh vien Family';
    }
}

async function addFamilyMember() {
    if (!elements.familyMemberIdentifier) return;
    const identifier = elements.familyMemberIdentifier.value.trim();
    if (!identifier) {
        showToast('⚠️', 'Nhap email hoac so dien thoai thanh vien');
        return;
    }

    try {
        const response = await fetch('/api/user/family/members', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ identifier })
        });
        const data = await response.json();
        if (data.success) {
            elements.familyMemberIdentifier.value = '';
            showToast('✅', 'Da them thanh vien vao goi Family');
            loadFamilyMembers();
        } else {
            showToast('❌', data.error || 'Khong them duoc thanh vien');
        }
    } catch (error) {
        console.error('Family add error:', error);
        showToast('❌', 'Loi them thanh vien Family');
    }
}

async function removeFamilyMember(familyMemberId) {
    if (!confirm('Xoa thanh vien nay khoi goi Family?')) return;
    try {
        const response = await fetch(`/api/user/family/members/${familyMemberId}`, { method: 'DELETE' });
        const data = await response.json();
        if (data.success) {
            showToast('✅', 'Da xoa thanh vien Family');
            loadFamilyMembers();
        } else {
            showToast('❌', data.error || 'Khong xoa duoc thanh vien');
        }
    } catch (error) {
        console.error('Family remove error:', error);
        showToast('❌', 'Loi xoa thanh vien Family');
    }
}

// ==========================================
// Onboarding & Profile Functions
// ==========================================
async function checkOnboarding() {
    try {
        if (state.currentUser) {
            if (state.currentUser.role === 'admin') {
                return;
            }
            const u = state.currentUser;
            const hasAccountProfile = !!(u.job && u.goal);
            if (!hasAccountProfile) {
                openModal('onboardingModal');
            }
            return;
        }
        return;
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
        if (state.currentUser) {
            const profile = {
                name: formData.name,
                age: formData.age,
                level: formData.level,
                goal: formData.goal,
                job: formData.job,
                english_usage: formData.field || '',
                meet_foreigners: false
            };
            const response = await fetch('/api/auth/profile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: state.currentUser.id, profile })
            });
            const data = await response.json();
            if (data.success) {
                state.currentUser = data.user;
                closeModal('onboardingModal');
                updateAuthUI();
                updateUserBadge();
                showToast('✅', `Da luu ho so cho ${formData.name}!`);
                updateWelcomeMessage(formData.name);
            } else {
                showToast('❌', data.error || 'Khong luu duoc ho so');
            }
            return;
        }

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
        }
    } catch (error) {
        console.error('Lỗi save onboarding:', error);
        showToast('❌', 'Có lỗi xảy ra. Em thử lại nhé!');
    }
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
    
    // Set radio button for meet_foreigners
    const meetForeignersRadios = document.querySelectorAll('input[name="profileMeetForeigners"]');
    meetForeignersRadios.forEach(radio => {
        radio.checked = (radio.value === 'true') === u.meet_foreigners;
    });
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
    elements.statsBtn.addEventListener('click', () => {
        loadStats();
        openModal('statsModal');
    });
    elements.startLessonBtn.addEventListener('click', () => openModal('lessonModal'));
    
    // Close modals
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const modal = e.target.closest('.modal');
            closeModal(modal.id);
        });
    });
    
    // Close modal when clicking outside
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal(modal.id);
        });
    });
    
    // Speaking practice
    elements.playPracticeBtn.addEventListener('click', () => {
        const text = elements.practiceText.textContent;
        speakText(text);
    });
    elements.recordPracticeBtn.addEventListener('click', togglePracticeRecording);
    
    // Profile button
    elements.profileBtn.addEventListener('click', () => {
        populateProfileForm();
        loadFamilyMembers();
        openModal('profileModal');
    });

    if (elements.addFamilyMemberBtn) {
        elements.addFamilyMemberBtn.addEventListener('click', addFamilyMember);
    }
    
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
            const formData = {
                user_id: state.currentUser.id,
                profile: {
                    name: document.getElementById('profileName').value,
                    age: document.getElementById('profileAge').value,
                    job: document.getElementById('profileJob').value,
                    meet_foreigners: document.querySelector('input[name="profileMeetForeigners"]:checked')?.value === 'true',
                    english_usage: document.getElementById('profileUsage').value,
                    goal: document.getElementById('profileGoal').value,
                    level: document.getElementById('profileLevel').value
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

    if (elements.plansBtn) {
        elements.plansBtn.addEventListener('click', openPlansModal);
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

async function loadInitialData() {
    // Kiểm tra kết nối server
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('Server status:', data.message);
    } catch (error) {
        console.error('Không kết nối được server:', error);
    }
    
    // Kiểm tra session hiện tại
    try {
        const response = await fetch('/api/auth/me');
        const data = await response.json();
        
        if (data.success) {
            state.currentUser = data.user;
            state.isGuest = false;
            updateAuthUI();
            updateUserBadge();
            await loadUserProfile();
            console.log('Restored session for user:', data.user.name);
        } else {
            state.isGuest = true;
            loadGuestLimits();
        }
    } catch (error) {
        console.error('Session check failed:', error);
        state.isGuest = true;
        loadGuestLimits();
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

function speakText(text) {
    if (!state.synthesis) {
        showToast('❌', 'Trình duyệt không hỗ trợ phát âm thanh.');
        return;
    }
    
    // Hủy các utterance đang chạy
    state.synthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 0.9;
    utterance.pitch = 1;
    
    // Tìm giọng tiếng Anh
    const voices = state.synthesis.getVoices();
    const englishVoice = voices.find(v => v.lang.startsWith('en'));
    if (englishVoice) {
        utterance.voice = englishVoice;
    }
    
    utterance.onend = () => {
        console.log('Speech finished');
    };
    
    utterance.onerror = (error) => {
        console.error('Speech error:', error);
    };
    
    state.synthesis.speak(utterance);
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
            body: JSON.stringify({ level: 'beginner' })
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
    let html = '';
    
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
                        <button class="speak-btn" onclick="speakText('${item.word}')">
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
                        <button class="speak-btn" onclick="speakText('${item.english.replace(/'/g, "\\'")}')">
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
                            <button class="speak-btn" onclick="speakText('${line.text.replace(/'/g, "\\'")}')">
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
                        <button class="btn btn-audio" onclick="speakText('${sentence.replace(/'/g, "\\'")}')">
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
    
    const profile = {
        age: document.getElementById('profileAge').value,
        job: document.getElementById('profileJob').value,
        meet_foreigners: document.querySelector('input[name="meetForeigners"]:checked').value === 'true',
        english_usage: document.getElementById('profileUsage').value,
        goal: document.getElementById('profileGoal').value,
        level: document.getElementById('profileLevel').value
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
        const response = await fetch(`/api/user/progress?user_id=${state.currentUser.id}`);
        const data = await response.json();
        
        if (data.success) {
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
    const errors = data.common_errors || [];
    const situations = progress.practiced_situations || [];
    
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
    const voices = speechSynthesis.getVoices();
    englishVoices = voices.filter(v => v.lang.startsWith('en'));
    console.log('English voices loaded:', englishVoices.length);
}

function speakText(text, rate = null) {
    if (!('speechSynthesis' in window)) {
        showToast('❌', 'Trình duyệt không hỗ trợ đọc văn bản');
        return;
    }
    
    // Cancel any ongoing speech
    speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Set voice to English if available
    if (englishVoices.length > 0) {
        // Prefer US English, then any English
        const usVoice = englishVoices.find(v => v.lang === 'en-US');
        utterance.voice = usVoice || englishVoices[0];
    }
    
    // Set rate (speed)
    utterance.rate = rate || state.ttsSpeed || 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    
    utterance.onstart = () => {
        state.isSpeaking = true;
        console.log('TTS started:', text.substring(0, 50));
    };
    
    utterance.onend = () => {
        state.isSpeaking = false;
    };
    
    utterance.onerror = (e) => {
        console.error('TTS error:', e);
        state.isSpeaking = false;
    };
    
    speechSynthesis.speak(utterance);
}

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
