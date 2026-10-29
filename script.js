/**
 * POTBHAR — script.js
 * Launch-Ready Product Site Logic
 * Plain Vanilla JavaScript — Zero External Heavy Libraries
 */

// =====================================================================
// CONFIG OBJECT — All editable values in ONE central location
// =====================================================================
const CONFIG = {
  phone: "+91 98765 43210",
  phoneRaw: "919876543210",
  whatsapp: "+91 98765 43210",
  whatsappRaw: "919876543210",
  email: "contact@potbhar.org",
  endpoint: "", // Backend form webhook or API endpoint (falls back to WhatsApp/mailto if empty)
  serviceArea: "Pune & Pimpri-Chinchwad (Expanding across Western Maharashtra)",
  operatingHours: "24/7 Rapid Surplus Response & Coordination",
  impact: {
    mealsServed: 24500,
    kgRecovered: 9800,
    partnerHomes: 38,
    donors: 142
  }
};

// =====================================================================
// I18N DICTIONARY — English / Hindi / Marathi
// =====================================================================
const I18N_DATA = {
  en: {
    nav_how: "How It Works",
    nav_quality: "Quality Check",
    nav_pathways: "Where Food Goes",
    nav_impact: "Impact",
    nav_faq: "FAQ",
    nav_contact: "Contact",
    nav_signin: "Sign In",
    nav_donate: "Donate Food",
    nav_register: "Register Shelter",
    hero_title: "Tonight, somewhere, a plate is empty. <span class=\"text-saffron\">Together, we make sure it gets filled.</span>",
    hero_sub: "Every day, surplus food from banquets, events, and restaurants goes to waste while nearby shelters struggle for fresh meals. POTBHAR collects excess food, checks its safety, and delivers it with care.",
    hero_btn_donate: "Donate Surplus Food",
    hero_btn_register: "Register Your Home / Shelter",
    trust_quality: "Quality-checked food",
    trust_delivery: "One-to-one delivery",
    trust_nowaste: "Nothing wasted"
  },
  hi: {
    nav_how: "यह कैसे काम करता है",
    nav_quality: "गुणवत्ता जांच",
    nav_pathways: "भोजन कहाँ जाता है",
    nav_impact: "हमारा प्रभाव",
    nav_faq: "सवाल-जवाब",
    nav_contact: "संपर्क करें",
    nav_signin: "लॉग इन",
    nav_donate: "भोजन दान करें",
    nav_register: "आश्रम जोड़ें",
    hero_title: "आज रात कहीं एक थाली खाली है। <span class=\"text-saffron\">साथ मिलकर हम इसे भरते हैं।</span>",
    hero_sub: "हर रोज़ शादियों, कार्यक्रमों और भोजनालयों से बचा हुआ शुद्ध भोजन बर्बाद होता है, जबकि नजदीकी आश्रमों में इसकी सख्त जरूरत होती है। पोटभर अतिरिक्त भोजन एकत्र कर, जांच कर सम्मानपूर्वक पहुंचाता है।",
    hero_btn_donate: "बचा हुआ भोजन दान करें",
    hero_btn_register: "अपना आश्रम / शेल्टर जोड़ें",
    trust_quality: "गुणवत्ता-जांचा भोजन",
    trust_delivery: "सीधा हाथों-हाथ वितरण",
    trust_nowaste: "कुछ भी बर्बाद नहीं"
  },
  mr: {
    nav_how: "हे कसे चालते",
    nav_quality: "अन्न दर्जा तपासणी",
    nav_pathways: "अन्न कोठे जाते",
    nav_impact: "कामाचा ठसा",
    nav_faq: "वारंवार विचारले जाणारे प्रश्न",
    nav_contact: "संपर्क",
    nav_signin: "लॉग इन",
    nav_donate: "अन्नदान करा",
    nav_register: "आश्रम नोंदणी करा",
    hero_title: "आज रात्री कुठे तरी एक ताट रिकामे आहे. <span class=\"text-saffron\">एकत्र येऊन आपण ते भरूया.</span>",
    hero_sub: "समारंभ, केटरर्स आणि हॉटेल्समधील अतिरिक्त सकस अन्न फेकून न देता, पोटभर ते गोळा करते, तपासणी करते आणि गरजू अनाथाश्रम व वृद्धाश्रमांपर्यंत प्रेमाने पोहोचवते.",
    hero_btn_donate: "अतिरिक्त अन्न दान करा",
    hero_btn_register: "आपल्या आश्रमाची नोंदणी करा",
    trust_quality: "दर्जा तपासलेले शुद्ध अन्न",
    trust_delivery: "थेट गरजूंपर्यंत वितरण",
    trust_nowaste: "अन्नाचा कणही वाया नाही"
  }
};

// =====================================================================
// INITIALIZATION ON DOM CONTENT LOADED
// =====================================================================
document.addEventListener("DOMContentLoaded", () => {
  initDynamicConfig();
  initLanguage();
  initNavigation();
  initScrollSpy();
  initScrollReveal();
  initImpactCounter();
  initQualityTickList();
  initWorkflowLine();
  initCalculator();
  initWhoIsItForTabs();
  initFaqAccordion();
  initModals();
  initForms();
  initBackToTop();
});

// Populate contact & config info into HTML dynamically
function initDynamicConfig() {
  // Service area and hours
  document.querySelectorAll("[data-config-phone]").forEach(el => {
    el.textContent = CONFIG.phone;
    if (el.tagName === "A") el.setAttribute("href", `tel:${CONFIG.phoneRaw}`);
  });
  document.querySelectorAll("[data-config-whatsapp]").forEach(el => {
    el.textContent = CONFIG.whatsapp;
    if (el.tagName === "A") el.setAttribute("href", `https://wa.me/${CONFIG.whatsappRaw}`);
  });
  document.querySelectorAll("[data-config-email]").forEach(el => {
    el.textContent = CONFIG.email;
    if (el.tagName === "A") el.setAttribute("href", `mailto:${CONFIG.email}`);
  });
  document.querySelectorAll("[data-config-area]").forEach(el => {
    el.textContent = CONFIG.serviceArea;
  });
  document.querySelectorAll("[data-config-hours]").forEach(el => {
    el.textContent = CONFIG.operatingHours;
  });

  // Hide impact section if numbers are missing/zero
  const impactSec = document.getElementById("impact");
  if (impactSec) {
    const hasValues = Object.values(CONFIG.impact).some(val => val && val > 0);
    if (!hasValues) {
      impactSec.style.display = "none";
    }
  }
}

// =====================================================================
// LANGUAGE SWITCHER (English / Hindi / Marathi)
// =====================================================================
function initLanguage() {
  const currentLang = localStorage.getItem("potbhar_lang") || "en";
  applyLanguage(currentLang);

  const langSelect = document.getElementById("languageSelect");
  if (langSelect) {
    langSelect.value = currentLang;
    langSelect.addEventListener("change", (e) => {
      const selected = e.target.value;
      localStorage.setItem("potbhar_lang", selected);
      applyLanguage(selected);
      showToast(`Language switched to ${e.target.options[e.target.selectedIndex].text}`);
    });
  }
}

function applyLanguage(lang) {
  const dict = I18N_DATA[lang] || I18N_DATA.en;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) {
      el.innerHTML = dict[key];
    }
  });
}

// =====================================================================
// NAVIGATION & MOBILE DRAWER
// =====================================================================
function initNavigation() {
  const header = document.querySelector(".site-header");
  const hamburgerBtn = document.getElementById("hamburgerBtn");
  const mobileDrawer = document.getElementById("mobileDrawer");
  const drawerCloseBtn = document.getElementById("drawerCloseBtn");
  const drawerLinks = document.querySelectorAll(".mobile-drawer-link");

  // Header shrink on scroll (h-20 -> h-16)
  window.addEventListener("scroll", () => {
    if (window.scrollY > 10) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  }, { passive: true });

  // Open drawer
  const openDrawer = () => {
    mobileDrawer.classList.add("open");
    hamburgerBtn.setAttribute("aria-expanded", "true");
    document.body.classList.add("drawer-locked");
    // Focus first link in drawer
    const firstFocusable = mobileDrawer.querySelector("a, button");
    if (firstFocusable) firstFocusable.focus();
  };

  // Close drawer
  const closeDrawer = () => {
    mobileDrawer.classList.remove("open");
    hamburgerBtn.setAttribute("aria-expanded", "false");
    document.body.classList.remove("drawer-locked");
    hamburgerBtn.focus();
  };

  if (hamburgerBtn) hamburgerBtn.addEventListener("click", openDrawer);
  if (drawerCloseBtn) drawerCloseBtn.addEventListener("click", closeDrawer);

  // Close drawer on link click
  drawerLinks.forEach(link => {
    link.addEventListener("click", closeDrawer);
  });

  // Close on outside click
  if (mobileDrawer) {
    mobileDrawer.addEventListener("click", (e) => {
      if (e.target === mobileDrawer) {
        closeDrawer();
      }
    });
  }

  // Close on Escape key and focus trap
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && mobileDrawer && mobileDrawer.classList.contains("open")) {
      closeDrawer();
    }
  });
}

// =====================================================================
// SCROLL-SPY WITH INTERSECTION OBSERVER
// =====================================================================
function initScrollSpy() {
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-link[href^='#']");

  if (!sections.length || !navLinks.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute("id");
        navLinks.forEach(link => {
          if (link.getAttribute("href") === `#${id}`) {
            link.classList.add("active");
          } else {
            link.classList.remove("active");
          }
        });
      }
    });
  }, {
    rootMargin: "-20% 0px -65% 0px"
  });

  sections.forEach(section => observer.observe(section));
}

// =====================================================================
// SCROLL REVEAL (data-reveal with stagger)
// =====================================================================
function initScrollReveal() {
  const revealElements = document.querySelectorAll("[data-reveal]");
  if (!revealElements.length) return;

  // Reduced motion check
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (prefersReduced) {
    revealElements.forEach(el => el.classList.add("revealed"));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const parent = entry.target.parentElement;
        const siblings = parent ? Array.from(parent.querySelectorAll("[data-reveal]")) : [];
        const index = siblings.indexOf(entry.target);
        const delay = index >= 0 ? index * 80 : 0;

        setTimeout(() => {
          entry.target.classList.add("revealed");
        }, delay);

        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: "0px 0px -40px 0px"
  });

  revealElements.forEach(el => observer.observe(el));
}

// =====================================================================
// IMPACT COUNT-UP (1.5s easeOutCubic)
// =====================================================================
function initImpactCounter() {
  const statElements = document.querySelectorAll("[data-stat-target]");
  if (!statElements.length) return;

  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const easeOutCubic = (t) => (--t) * t * t + 1;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        statElements.forEach(el => {
          const key = el.getAttribute("data-stat-target");
          const targetValue = CONFIG.impact[key] || 0;

          if (prefersReduced) {
            el.textContent = targetValue.toLocaleString("en-IN");
            return;
          }

          const duration = 1500; // 1.5 seconds
          const startTime = performance.now();

          const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = easeOutCubic(progress);
            const currentCount = Math.floor(eased * targetValue);

            el.textContent = currentCount.toLocaleString("en-IN");

            if (progress < 1) {
              requestAnimationFrame(animate);
            } else {
              el.textContent = targetValue.toLocaleString("en-IN");
            }
          };

          requestAnimationFrame(animate);
        });

        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.25 });

  const impactSection = document.getElementById("impact");
  if (impactSection) observer.observe(impactSection);
}

// =====================================================================
// QUALITY CHECKLIST TICKS IN ON SCROLL
// =====================================================================
function initQualityTickList() {
  const checkItems = document.querySelectorAll(".check-item");
  const qualitySection = document.getElementById("quality");
  if (!checkItems.length || !qualitySection) return;

  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (prefersReduced) {
    checkItems.forEach(item => item.classList.add("ticked"));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        checkItems.forEach((item, index) => {
          setTimeout(() => {
            item.classList.add("ticked");
          }, index * 180);
        });
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  observer.observe(qualitySection);
}

// =====================================================================
// HOW IT WORKS CONNECTING LINE
// =====================================================================
function initWorkflowLine() {
  const lineProgress = document.getElementById("workflowLineProgress");
  const stepsContainer = document.getElementById("how-it-works");
  if (!lineProgress || !stepsContainer) return;

  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (prefersReduced) {
    lineProgress.style.width = "100%";
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        lineProgress.style.width = "100%";
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  observer.observe(stepsContainer);
}

// =====================================================================
// IMPACT CALCULATOR (Estimating 400g / plate)
// =====================================================================
function initCalculator() {
  const slider = document.getElementById("calcKgSlider");
  const kgDisplay = document.getElementById("calcKgDisplay");
  const peopleFedDisplay = document.getElementById("calcPeopleFed");
  const compostDisplay = document.getElementById("calcCompostKg");
  const pickupBtn = document.getElementById("calcPickupBtn");

  if (!slider) return;

  const updateCalc = () => {
    const kg = parseInt(slider.value, 10) || 50;
    if (kgDisplay) kgDisplay.textContent = `${kg} kg`;

    // 400 grams per plate standard Indian serving calculation
    const peopleFed = Math.floor((kg * 1000) / 400);
    // Estimated soil compost produced if organic waste diverted (~35%)
    const compostKg = Math.round(kg * 0.35);

    if (peopleFedDisplay) peopleFedDisplay.textContent = peopleFed.toLocaleString("en-IN");
    if (compostDisplay) compostDisplay.textContent = compostKg.toLocaleString("en-IN");
  };

  slider.addEventListener("input", updateCalc);
  updateCalc();

  // Button opens Donor modal with quantity pre-filled
  if (pickupBtn) {
    pickupBtn.addEventListener("click", () => {
      const kg = slider.value;
      const donorQtyInput = document.getElementById("donorQuantity");
      if (donorQtyInput) {
        donorQtyInput.value = kg;
      }
      openModal("modalDonor");
    });
  }
}

// =====================================================================
// WHO IS IT FOR TABS
// =====================================================================
function initWhoIsItForTabs() {
  const tabButtons = document.querySelectorAll(".tab-button");
  const tabPanes = document.querySelectorAll(".tab-pane");

  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const target = btn.getAttribute("data-tab");

      tabButtons.forEach(b => {
        b.classList.remove("active");
        b.setAttribute("aria-selected", "false");
      });
      tabPanes.forEach(p => p.classList.remove("active"));

      btn.classList.add("active");
      btn.setAttribute("aria-selected", "true");

      const activePane = document.getElementById(target);
      if (activePane) {
        activePane.classList.add("active");
      }
    });
  });
}

// =====================================================================
// FAQ ACCORDION (Smooth Height Transition)
// =====================================================================
function initFaqAccordion() {
  const faqItems = document.querySelectorAll(".faq-item");

  faqItems.forEach(item => {
    const trigger = item.querySelector(".faq-trigger");
    const content = item.querySelector(".faq-content");

    if (trigger && content) {
      trigger.addEventListener("click", () => {
        const isOpen = item.classList.contains("open");

        // Optional: close other open items
        faqItems.forEach(other => {
          if (other !== item && other.classList.contains("open")) {
            other.classList.remove("open");
            other.querySelector(".faq-trigger").setAttribute("aria-expanded", "false");
            other.querySelector(".faq-content").style.maxHeight = null;
          }
        });

        if (isOpen) {
          item.classList.remove("open");
          trigger.setAttribute("aria-expanded", "false");
          content.style.maxHeight = null;
        } else {
          item.classList.add("open");
          trigger.setAttribute("aria-expanded", "true");
          content.style.maxHeight = content.scrollHeight + "px";
        }
      });
    }
  });
}

// =====================================================================
// MODAL SYSTEM (Donor, Recipient, Volunteer, Sign In, Privacy, Terms)
// =====================================================================
let lastActiveTrigger = null;

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (!modal) return;

  lastActiveTrigger = document.activeElement;
  modal.classList.add("active");
  modal.setAttribute("aria-hidden", "false");
  document.body.classList.add("modal-open");

  // Auto-focus first input
  setTimeout(() => {
    const firstInput = modal.querySelector("input, select, textarea, button");
    if (firstInput) firstInput.focus();
  }, 100);
}

function closeModal(modal) {
  if (!modal) return;
  modal.classList.remove("active");
  modal.setAttribute("aria-hidden", "true");
  document.body.classList.remove("modal-open");

  if (lastActiveTrigger) {
    lastActiveTrigger.focus();
    lastActiveTrigger = null;
  }
}

function initModals() {
  // Triggers
  document.querySelectorAll("[data-open-modal]").forEach(trigger => {
    trigger.addEventListener("click", (e) => {
      e.preventDefault();
      const modalId = trigger.getAttribute("data-open-modal");
      openModal(modalId);
    });
  });

  // Close buttons and overlay clicks
  document.querySelectorAll(".modal-overlay").forEach(modal => {
    const closeBtn = modal.querySelector(".modal-close-btn");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => closeModal(modal));
    }

    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        closeModal(modal);
      }
    });
  });

  // Esc key closes any open modal
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      const openModalEl = document.querySelector(".modal-overlay.active");
      if (openModalEl) closeModal(openModalEl);
    }
  });
}

// =====================================================================
// FORMS HANDLING & VALIDATION
// =====================================================================
function initForms() {
  // Auto-fill donor details from localStorage
  const savedDonor = localStorage.getItem("potbhar_donor");
  if (savedDonor) {
    try {
      const data = JSON.parse(savedDonor);
      const nameInput = document.getElementById("donorName");
      const phoneInput = document.getElementById("donorPhone");
      const addrInput = document.getElementById("donorAddress");
      if (nameInput && data.name) nameInput.value = data.name;
      if (phoneInput && data.phone) phoneInput.value = data.phone;
      if (addrInput && data.address) addrInput.value = data.address;
    } catch (e) {
      // Ignore parse errors
    }
  }

  // 1. Donor Form Submission
  const donorForm = document.getElementById("donorForm");
  if (donorForm) {
    donorForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!validateForm(donorForm)) return;

      const submitBtn = donorForm.querySelector("button[type='submit']");
      setButtonLoading(submitBtn, true);

      const formData = {
        name: donorForm.donorName.value.trim(),
        phone: donorForm.donorPhone.value.trim(),
        address: donorForm.donorAddress.value.trim(),
        foodType: donorForm.donorFoodType.value,
        quantityKg: donorForm.donorQuantity.value,
        cookedTime: donorForm.donorCookedTime.value.trim(),
        pickupTime: donorForm.donorPickupTime.value.trim()
      };

      // Save for repeat donors
      localStorage.setItem("potbhar_donor", JSON.stringify({
        name: formData.name,
        phone: formData.phone,
        address: formData.address
      }));

      await handleFormDispatch("Surplus Food Donation", formData, submitBtn, donorForm, "modalDonor");
    });
  }

  // 2. Recipient Form Submission
  const recipientForm = document.getElementById("recipientForm");
  if (recipientForm) {
    recipientForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!validateForm(recipientForm)) return;

      const submitBtn = recipientForm.querySelector("button[type='submit']");
      setButtonLoading(submitBtn, true);

      const formData = {
        orgName: recipientForm.orgName.value.trim(),
        orgType: recipientForm.orgType.value,
        contactPerson: recipientForm.contactPerson.value.trim(),
        phone: recipientForm.recipientPhone.value.trim(),
        address: recipientForm.recipientAddress.value.trim(),
        peopleServed: recipientForm.peopleServed.value
      };

      await handleFormDispatch("Recipient Shelter Registration", formData, submitBtn, recipientForm, "modalRecipient");
    });
  }

  // 3. Volunteer Form Submission
  const volunteerForm = document.getElementById("volunteerForm");
  if (volunteerForm) {
    volunteerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!validateForm(volunteerForm)) return;

      const submitBtn = volunteerForm.querySelector("button[type='submit']");
      setButtonLoading(submitBtn, true);

      const formData = {
        name: volunteerForm.volunteerName.value.trim(),
        phone: volunteerForm.volunteerPhone.value.trim(),
        area: volunteerForm.volunteerArea.value.trim(),
        availability: volunteerForm.volunteerAvailability.value,
        hasVehicle: volunteerForm.volunteerVehicle.value
      };

      await handleFormDispatch("Volunteer Application", formData, submitBtn, volunteerForm, "modalVolunteer");
    });
  }

  // 4. Sign In Form
  const signinForm = document.getElementById("signinForm");
  if (signinForm) {
    signinForm.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!validateForm(signinForm)) return;

      const submitBtn = signinForm.querySelector("button[type='submit']");
      setButtonLoading(submitBtn, true);

      setTimeout(() => {
        setButtonLoading(submitBtn, false);
        const modal = document.getElementById("modalSignIn");
        closeModal(modal);
        showToast("Signed in successfully. Welcome to POTBHAR.");
      }, 700);
    });
  }
}

// Inline Form Validation
function validateForm(form) {
  let isValid = true;
  const groups = form.querySelectorAll(".form-group");

  groups.forEach(group => {
    const input = group.querySelector("input, select, textarea");
    if (!input) return;

    group.classList.remove("has-error");

    // Required check
    if (input.hasAttribute("required")) {
      if (input.type === "checkbox" && !input.checked) {
        group.classList.add("has-error");
        isValid = false;
      } else if (!input.value.trim()) {
        group.classList.add("has-error");
        isValid = false;
      }
    }

    // Phone 10-digit validation
    if (input.type === "tel" || input.name.toLowerCase().includes("phone")) {
      const phoneVal = input.value.replace(/\D/g, "");
      if (phoneVal.length !== 10) {
        group.classList.add("has-error");
        const errMsg = group.querySelector(".form-error-msg");
        if (errMsg) errMsg.textContent = "Please enter a valid 10-digit Indian phone number.";
        isValid = false;
      }
    }
  });

  return isValid;
}

// Dispatch to Config Endpoint or Fallback to WhatsApp
async function handleFormDispatch(subject, data, btn, form, modalId) {
  let endpointSuccess = false;

  if (CONFIG.endpoint) {
    try {
      const res = await fetch(CONFIG.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subject, data, timestamp: new Date().toISOString() })
      });
      if (res.ok) endpointSuccess = true;
    } catch (err) {
      console.warn("Backend endpoint unreachable, falling back to WhatsApp dispatch:", err);
    }
  }

  setButtonLoading(btn, false);
  const modal = document.getElementById(modalId);

  // If no backend endpoint or endpoint failed, open WhatsApp with pre-filled message
  if (!endpointSuccess) {
    let msgText = `*POTBHAR: ${subject}*\n\n`;
    for (const [key, val] of Object.entries(data)) {
      msgText += `• ${key}: ${val}\n`;
    }
    const encoded = encodeURIComponent(msgText);
    const waUrl = `https://wa.me/${CONFIG.whatsappRaw}?text=${encoded}`;
    window.open(waUrl, "_blank");
  }

  closeModal(modal);
  showToast("Thank you. We will call you within 30 minutes.");
  form.reset();
}

function setButtonLoading(btn, isLoading) {
  if (!btn) return;
  if (isLoading) {
    btn.disabled = true;
    btn.dataset.originalText = btn.innerHTML;
    btn.innerHTML = `<span class="spinner"></span> Processing...`;
  } else {
    btn.disabled = false;
    if (btn.dataset.originalText) {
      btn.innerHTML = btn.dataset.originalText;
    }
  }
}

// =====================================================================
// TOAST NOTIFICATIONS (Slide up, 3s duration)
// =====================================================================
let toastTimeout = null;

function showToast(message) {
  let toastContainer = document.querySelector(".toast-container");
  if (!toastContainer) {
    toastContainer = document.createElement("div");
    toastContainer.className = "toast-container";
    document.body.appendChild(toastContainer);
  }

  toastContainer.innerHTML = `
    <div class="toast-msg">
      <i class="fa-solid fa-circle-check text-leaf"></i>
      <span>${message}</span>
    </div>
  `;

  const msgEl = toastContainer.querySelector(".toast-msg");
  setTimeout(() => msgEl.classList.add("show"), 10);

  if (toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    msgEl.classList.remove("show");
  }, 3000);
}

// =====================================================================
// BACK TO TOP BUTTON (Appears after 600px)
// =====================================================================
function initBackToTop() {
  const btn = document.getElementById("backToTopBtn");
  if (!btn) return;

  window.addEventListener("scroll", () => {
    if (window.scrollY > 600) {
      btn.classList.add("visible");
    } else {
      btn.classList.remove("visible");
    }
  }, { passive: true });

  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}
