// 탭 네비게이션 기능
document.addEventListener('DOMContentLoaded', function() {
    initializeTabNavigation();
    initializeInteractiveFeatures();
    initializeProgressTracking();
    initializePrintFunctionality();
});

// 탭 네비게이션 초기화
function initializeTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // 모든 탭 버튼과 콘텐츠에서 active 클래스 제거
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // 클릭된 탭 버튼과 해당 콘텐츠에 active 클래스 추가
            this.classList.add('active');
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
                
                // 탭 전환 시 스크롤을 맨 위로
                targetContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
                
                // 로컬 스토리지에 현재 탭 저장
                localStorage.setItem('currentTab', targetTab);
                
                // 탭 전환 애니메이션
                animateTabTransition(targetContent);
            }
        });
    });
    
    // 페이지 로드 시 저장된 탭 복원 또는 기본 탭 설정
    const savedTab = localStorage.getItem('currentTab');
    if (savedTab && document.getElementById(savedTab)) {
        const savedButton = document.querySelector(`[data-tab="${savedTab}"]`);
        if (savedButton) {
            savedButton.click();
        }
    }
}

// 탭 전환 애니메이션
function animateTabTransition(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        element.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 50);
}

// 인터랙티브 기능 초기화
function initializeInteractiveFeatures() {
    // 체크리스트 기능
    initializeCheckboxes();
    
    // 카드 호버 효과
    initializeCardEffects();
    
    // 스크롤 애니메이션
    initializeScrollAnimations();
    
    // 툴팁 기능
    initializeTooltips();
    
    // 검색 기능
    initializeSearchFunction();
}

// 체크박스 상태 저장 및 복원
function initializeCheckboxes() {
    const checkboxes = document.querySelectorAll('.checklist input[type="checkbox"]');
    
    checkboxes.forEach((checkbox, index) => {
        // 저장된 상태 복원
        const savedState = localStorage.getItem(`checkbox_${index}`);
        if (savedState === 'true') {
            checkbox.checked = true;
            animateCheckbox(checkbox);
        }
        
        // 상태 변경 시 저장
        checkbox.addEventListener('change', function() {
            localStorage.setItem(`checkbox_${index}`, this.checked);
            animateCheckbox(this);
            updateCheckboxProgress();
        });
    });
    
    updateCheckboxProgress();
}

// 체크박스 애니메이션
function animateCheckbox(checkbox) {
    const label = checkbox.parentElement;
    if (checkbox.checked) {
        label.style.background = 'linear-gradient(135deg, #d4edda, #c3e6cb)';
        label.style.color = '#155724';
        label.style.transform = 'scale(1.02)';
        
        // 체크 사운드 효과 (선택사항)
        playCheckSound();
    } else {
        label.style.background = '';
        label.style.color = '';
        label.style.transform = 'scale(1)';
    }
}

// 체크박스 진행률 업데이트
function updateCheckboxProgress() {
    const checkboxes = document.querySelectorAll('.checklist input[type="checkbox"]');
    const checkedCount = document.querySelectorAll('.checklist input[type="checkbox"]:checked').length;
    const totalCount = checkboxes.length;
    const progressPercentage = totalCount > 0 ? (checkedCount / totalCount) * 100 : 0;
    
    // 진행률 표시 요소가 있다면 업데이트
    const progressElements = document.querySelectorAll('.checkbox-progress');
    progressElements.forEach(element => {
        element.textContent = `${checkedCount}/${totalCount} 완료 (${Math.round(progressPercentage)}%)`;
    });
}

// 카드 효과 초기화
function initializeCardEffects() {
    const cards = document.querySelectorAll('.overview-card, .material-card, .assessment-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.15)';
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        });
    });
}

// 스크롤 애니메이션 초기화
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // 타임라인 아이템 순차 애니메이션
                if (entry.target.classList.contains('timeline-item')) {
                    animateTimelineItem(entry.target);
                }
            }
        });
    }, observerOptions);
    
    // 관찰할 요소들 등록
    const animatableElements = document.querySelectorAll(
        '.overview-card, .timeline-item, .material-card, .assessment-card'
    );
    
    animatableElements.forEach(element => {
        observer.observe(element);
    });
}

// 타임라인 아이템 애니메이션
function animateTimelineItem(item) {
    const timeMarker = item.querySelector('.time-marker');
    const content = item.querySelector('.timeline-content');
    
    if (timeMarker) {
        setTimeout(() => {
            timeMarker.style.transform = 'scale(1.1)';
            timeMarker.style.boxShadow = '0 0 20px rgba(102, 126, 234, 0.4)';
        }, 200);
        
        setTimeout(() => {
            timeMarker.style.transform = 'scale(1)';
        }, 600);
    }
    
    if (content) {
        content.style.animation = 'slideInLeft 0.6s ease-out forwards';
    }
}

// 툴팁 기능 초기화
function initializeTooltips() {
    // 약어나 전문용어에 대한 툴팁 추가
    const tooltipTerms = {
        'AI': '인공지능(Artificial Intelligence)',
        '지도학습': '정답이 있는 데이터로 학습하는 방법',
        '비지도학습': '정답이 없는 데이터에서 패턴을 찾는 방법',
        '클러스터링': '비슷한 특성의 데이터를 그룹화하는 기법',
        '분류': '데이터를 미리 정의된 카테고리로 구분하는 작업',
        '회귀': '연속적인 수치값을 예측하는 작업'
    };
    
        Object.keys(tooltipTerms).forEach(term => {
        const textNodes = findTextNodes(document.body, term);
        textNodes.forEach(node => {
            createTooltip(node, term, tooltipTerms[term]);
        });
    });
}

// 텍스트 노드에서 특정 용어 찾기
function findTextNodes(element, searchTerm) {
    const walker = document.createTreeWalker(
        element,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    const matchingNodes = [];
    let node;
    
    while (node = walker.nextNode()) {
        if (node.textContent.includes(searchTerm) && 
            !node.parentElement.classList.contains('tooltip-term')) {
            matchingNodes.push(node);
        }
    }
    
    return matchingNodes;
}

// 툴팁 생성
function createTooltip(textNode, term, description) {
    const parent = textNode.parentElement;
    const text = textNode.textContent;
    const index = text.indexOf(term);
    
    if (index === -1) return;
    
    const beforeText = text.substring(0, index);
    const afterText = text.substring(index + term.length);
    
    const wrapper = document.createElement('span');
    wrapper.className = 'tooltip-container';
    wrapper.innerHTML = `
        ${beforeText}
        <span class="tooltip-term" data-tooltip="${description}">
            ${term}
            <span class="tooltip-popup">${description}</span>
        </span>
        ${afterText}
    `;
    
    parent.replaceChild(wrapper, textNode);
}

// 진행률 추적 초기화
function initializeProgressTracking() {
    // 읽기 진행률 추적
    trackReadingProgress();
    
    // 학습 시간 추적
    trackLearningTime();
    
    // 인터랙션 추적
    trackUserInteractions();
}

// 읽기 진행률 추적
function trackReadingProgress() {
    const sections = document.querySelectorAll('.tab-content');
    let readingSessions = JSON.parse(localStorage.getItem('readingSessions') || '{}');
    
    sections.forEach(section => {
        const sectionId = section.id;
        if (!readingSessions[sectionId]) {
            readingSessions[sectionId] = {
                visits: 0,
                timeSpent: 0,
                lastVisit: null
            };
        }
        
        // 섹션이 활성화될 때마다 기록
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting && entry.target.classList.contains('active')) {
                    const sessionStart = Date.now();
                    readingSessions[sectionId].visits++;
                    readingSessions[sectionId].lastVisit = sessionStart;
                    
                    // 섹션을 벗어날 때 시간 기록
                    const exitObserver = new IntersectionObserver(function(exitEntries) {
                        exitEntries.forEach(exitEntry => {
                            if (!exitEntry.isIntersecting) {
                                const timeSpent = Date.now() - sessionStart;
                                readingSessions[sectionId].timeSpent += timeSpent;
                                localStorage.setItem('readingSessions', JSON.stringify(readingSessions));
                                exitObserver.disconnect();
                            }
                        });
                    });
                    
                    exitObserver.observe(entry.target);
                }
            });
        });
        
        observer.observe(section);
    });
}

// 학습 시간 추적
function trackLearningTime() {
    let totalLearningTime = parseInt(localStorage.getItem('totalLearningTime') || '0');
    let sessionStartTime = Date.now();
    let isActive = true;
    
    // 페이지 활성화/비활성화 감지
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            if (isActive) {
                totalLearningTime += Date.now() - sessionStartTime;
                localStorage.setItem('totalLearningTime', totalLearningTime.toString());
                isActive = false;
            }
        } else {
            sessionStartTime = Date.now();
            isActive = true;
        }
    });
    
    // 페이지 언로드 시 시간 저장
    window.addEventListener('beforeunload', function() {
        if (isActive) {
            totalLearningTime += Date.now() - sessionStartTime;
            localStorage.setItem('totalLearningTime', totalLearningTime.toString());
        }
    });
    
    // 학습 시간 표시 업데이트
    updateLearningTimeDisplay();
    setInterval(updateLearningTimeDisplay, 60000); // 1분마다 업데이트
}

// 학습 시간 표시 업데이트
function updateLearningTimeDisplay() {
    const totalTime = parseInt(localStorage.getItem('totalLearningTime') || '0');
    const currentSessionTime = Date.now() - (parseInt(localStorage.getItem('sessionStartTime')) || Date.now());
    const totalMinutes = Math.floor((totalTime + currentSessionTime) / 60000);
    
    // 학습 시간 표시 요소가 있다면 업데이트
    const timeDisplays = document.querySelectorAll('.learning-time-display');
    timeDisplays.forEach(display => {
        display.textContent = `총 학습 시간: ${totalMinutes}분`;
    });
}

// 사용자 인터랙션 추적
function trackUserInteractions() {
    let interactions = JSON.parse(localStorage.getItem('userInteractions') || '{}');
    
    // 클릭 이벤트 추적
    document.addEventListener('click', function(e) {
        const targetElement = e.target;
        const elementType = targetElement.tagName.toLowerCase();
        const elementClass = targetElement.className;
        
        if (!interactions.clicks) interactions.clicks = {};
        if (!interactions.clicks[elementType]) interactions.clicks[elementType] = 0;
        
        interactions.clicks[elementType]++;
        
        // 특별한 요소들 개별 추적
        if (elementClass.includes('tab-btn')) {
            if (!interactions.tabSwitches) interactions.tabSwitches = 0;
            interactions.tabSwitches++;
        }
        
        if (elementClass.includes('overview-card') || elementClass.includes('material-card')) {
            if (!interactions.cardClicks) interactions.cardClicks = 0;
            interactions.cardClicks++;
        }
        
        localStorage.setItem('userInteractions', JSON.stringify(interactions));
    });
    
    // 스크롤 깊이 추적
    let maxScrollDepth = 0;
    window.addEventListener('scroll', function() {
        const scrollDepth = (window.scrollY + window.innerHeight) / document.body.scrollHeight;
        maxScrollDepth = Math.max(maxScrollDepth, scrollDepth);
        
        interactions.maxScrollDepth = maxScrollDepth;
        localStorage.setItem('userInteractions', JSON.stringify(interactions));
    });
}

// 프린트 기능 초기화
function initializePrintFunctionality() {
    // 프린트 버튼 추가
    addPrintButton();
    
    // 프린트 스타일 최적화
    optimizePrintStyles();
}

// 프린트 버튼 추가
function addPrintButton() {
    const header = document.querySelector('.lesson-header');
    if (header) {
        const printButton = document.createElement('button');
        printButton.innerHTML = '🖨️ 인쇄하기';
        printButton.className = 'print-button';
        printButton.style.cssText = `
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            cursor: pointer;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            font-size: 0.9rem;
            z-index: 10;
        `;
        
        printButton.addEventListener('click', function() {
            // 모든 탭 내용을 표시
            showAllTabsForPrint();
            
            // 프린트 대화상자 열기
            setTimeout(() => {
                window.print();
                
                // 프린트 후 원래 상태로 복원
                setTimeout(() => {
                    restoreTabsAfterPrint();
                }, 1000);
            }, 500);
        });
        
        printButton.addEventListener('mouseenter', function() {
            this.style.background = 'rgba(255, 255, 255, 0.3)';
            this.style.transform = 'scale(1.05)';
        });
        
        printButton.addEventListener('mouseleave', function() {
            this.style.background = 'rgba(255, 255, 255, 0.2)';
            this.style.transform = 'scale(1)';
        });
        
        header.appendChild(printButton);
    }
}

// 프린트용 모든 탭 표시
function showAllTabsForPrint() {
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.style.display = 'block';
        content.classList.add('print-visible');
    });
}

// 프린트 후 탭 상태 복원
function restoreTabsAfterPrint() {
    const tabContents = document.querySelectorAll('.tab-content');
    const activeTab = document.querySelector('.tab-btn.active').getAttribute('data-tab');
    
    tabContents.forEach(content => {
        content.classList.remove('print-visible');
        if (content.id !== activeTab) {
            content.style.display = 'none';
        }
    });
}

// 프린트 스타일 최적화
function optimizePrintStyles() {
    // 동적 프린트 스타일 추가
    const printStyles = document.createElement('style');
    printStyles.setAttribute('media', 'print');
    printStyles.textContent = `
        @page {
            margin: 2cm;
            size: A4;
        }
        
        .print-visible {
            display: block !important;
            page-break-before: always;
        }
        
        .print-visible:first-child {
            page-break-before: auto;
        }
        
        .timeline-item {
            page-break-inside: avoid;
            margin-bottom: 1rem;
        }
        
        .overview-card,
        .material-card,
        .assessment-card {
            page-break-inside: avoid;
            margin-bottom: 1rem;
        }
        
        .lesson-header {
            page-break-after: always;
        }
        
        .print-button {
            display: none !important;
        }
    `;
    
    document.head.appendChild(printStyles);
}

// 검색 기능 초기화
function initializeSearchFunction() {
    // 검색 박스 추가
    addSearchBox();
    
    // 검색 기능 구현
    implementSearch();
}

// 검색 박스 추가
function addSearchBox() {
    const header = document.querySelector('.lesson-header');
    if (header) {
        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container';
        searchContainer.style.cssText = `
            position: absolute;
            top: 1rem;
            left: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            z-index: 10;
        `;
        
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = '내용 검색...';
        searchInput.className = 'search-input';
        searchInput.style.cssText = `
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 0.5rem;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            width: 200px;
            font-size: 0.9rem;
        `;
        
        searchInput.addEventListener('input', function() {
            performSearch(this.value.trim());
        });
        
        const clearButton = document.createElement('button');
        clearButton.innerHTML = '✕';
        clearButton.className = 'search-clear';
        clearButton.style.cssText = `
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 0.5rem;
            border-radius: 50%;
            cursor: pointer;
            backdrop-filter: blur(10px);
            width: 35px;
            height: 35px;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        
        clearButton.addEventListener('click', function() {
            searchInput.value = '';
            clearSearchHighlights();
        });
        
        searchContainer.appendChild(searchInput);
        searchContainer.appendChild(clearButton);
        header.appendChild(searchContainer);
    }
}

// 검색 수행
function performSearch(query) {
    clearSearchHighlights();
    
    if (query.length < 2) return;
    
    const regex = new RegExp(`(${query})`, 'gi');
    const walker = document.createTreeWalker(
        document.querySelector('.container'),
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    let node;
    const matches = [];
    
    while (node = walker.nextNode()) {
        if (node.textContent.match(regex)) {
            matches.push(node);
        }
    }
    
    matches.forEach(node => highlightSearchMatch(node, regex));
    
    // 첫 번째 매치로 스크롤
    if (matches.length > 0) {
        const firstHighlight = document.querySelector('.search-highlight');
        if (firstHighlight) {
            firstHighlight.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

// 검색 결과 하이라이트
function highlightSearchMatch(textNode, regex) {
    const parent = textNode.parentElement;
    const text = textNode.textContent;
    const highlightedText = text.replace(regex, '<mark class="search-highlight">$1</mark>');
    
    const wrapper = document.createElement('span');
    wrapper.innerHTML = highlightedText;
    
    parent.replaceChild(wrapper, textNode);
}

// 검색 하이라이트 제거
function clearSearchHighlights() {
    const highlights = document.querySelectorAll('.search-highlight');
    highlights.forEach(highlight => {
        const parent = highlight.parentElement;
        parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
        parent.normalize();
    });
}

// 사운드 효과 (선택사항)
function playCheckSound() {
    // Web Audio API를 사용한 간단한 체크 사운드
    if (typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined') {
        const audioContext = new (AudioContext || webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        oscillator.frequency.setValueAtTime(1000, audioContext.currentTime + 0.1);
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.2);
    }
}

// 다크 모드 토글 (선택사항)
function initializeDarkMode() {
    const darkModeToggle = document.createElement('button');
    darkModeToggle.innerHTML = '🌙';
    darkModeToggle.className = 'dark-mode-toggle';
    darkModeToggle.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: #667eea;
        border: none;
        color: white;
        padding: 1rem;
        border-radius: 50%;
        cursor: pointer;
        font-size: 1.2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        z-index: 1000;
    `;
    
    darkModeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        this.innerHTML = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
        
        // 다크 모드 상태 저장
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
    });
    
    // 저장된 다크 모드 상태 복원
    const savedDarkMode = localStorage.getItem('darkMode') === 'true';
    if (savedDarkMode) {
        document.body.classList.add('dark-mode');
        darkModeToggle.innerHTML = '☀️';
    }
    
    document.body.appendChild(darkModeToggle);
}

// 학습 진행률 대시보드
function createProgressDashboard() {
    const dashboard = document.createElement('div');
    dashboard.className = 'progress-dashboard';
    dashboard.style.cssText = `
        position: fixed;
        bottom: 2rem;
        left: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        min-width: 200px;
        z-index: 1000;
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    `;
    
    const toggleButton = document.createElement('button');
    toggleButton.innerHTML = '📊';
    toggleButton.style.cssText = `
        position: absolute;
        right: -40px;
        top: 50%;
        transform: translateY(-50%);
        background: #667eea;
        border: none;
        color: white;
        padding: 0.5rem;
        border-radius: 0 8px 8px 0;
        cursor: pointer;
    `;
    
    let isOpen = false;
    toggleButton.addEventListener('click', function() {
        isOpen = !isOpen;
        dashboard.style.transform = isOpen ? 'translateX(0)' : 'translateX(-100%)';
    });
    
    dashboard.appendChild(toggleButton);
    
    // 진행률 내용 업데이트
    updateProgressDashboard(dashboard);
    
    document.body.appendChild(dashboard);
    
    // 주기적으로 대시보드 업데이트
    setInterval(() => updateProgressDashboard(dashboard), 30000);
}

function updateProgressDashboard(dashboard) {
    const content = dashboard.querySelector('.dashboard-content') || document.createElement('div');
    content.className = 'dashboard-content';
    
    const readingSessions = JSON.parse(localStorage.getItem('readingSessions') || '{}');
    const totalTime = parseInt(localStorage.getItem('totalLearningTime') || '0');
    const interactions = JSON.parse(localStorage.getItem('userInteractions') || '{}');
    
    content.innerHTML = `
        <h4 style="margin: 0 0 1rem 0; color: #667eea;">학습 진행률</h4>
        <div style="margin-bottom: 0.5rem;">
            <small>총 학습 시간: ${Math.floor(totalTime / 60000)}분</small>
        </div>
        <div style="margin-bottom: 0.5rem;">
            <small>탭 전환: ${interactions.tabSwitches || 0}회</small>
        </div>
        <div style="margin-bottom: 0.5rem;">
            <small>스크롤 깊이: ${Math.round((interactions.maxScrollDepth || 0) * 100)}%</small>
        </div>
        <div style="margin-bottom: 0.5rem;">
            <small>카드 클릭: ${interactions.cardClicks || 0}회</small>
        </div>
    `;
    
    if (!dashboard.querySelector('.dashboard-content')) {
        dashboard.appendChild(content);
    }
}

// 초기화 함수 실행
document.addEventListener('DOMContentLoaded', function() {
    // 기본 기능들
    initializeTabNavigation();
    initializeInteractiveFeatures();
    initializeProgressTracking();
    initializePrintFunctionality();
    
    // 추가 기능들 (선택사항)
    initializeDarkMode();
    createProgressDashboard();
});