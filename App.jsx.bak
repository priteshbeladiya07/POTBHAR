import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  ShieldCheck,
  AlertTriangle,
  HeartHandshake,
  Leaf,
  Truck,
  Flame,
  CheckCircle2,
  Clock,
  Thermometer,
  Camera,
  UploadCloud,
  ChevronRight,
  X,
  Menu,
  ArrowRight,
  Search,
  Filter,
  Sparkles,
  TrendingUp,
  BarChart3,
  Award,
  Info,
  Lock,
  User,
  Layers,
  RotateCcw,
  Check,
  HelpCircle,
  FileCheck,
  Building2,
  MapPin,
  Utensils
} from 'lucide-react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  AreaChart,
  Area,
  Legend
} from 'recharts';

// ==========================================
// SAMPLE DATA & CONSTANTS (STRICTLY FICTIONAL)
// ==========================================

const SAMPLE_BATCHES_INITIAL = [
  {
    id: 'BATCH-401',
    kitchen: 'Saffron Hall Caterers',
    category: 'Cooked Grain (Biryani & Pulao)',
    weightKg: 85,
    temp: '63.5°C',
    hoursSinceCooked: 2.5,
    container: 'Insulated Stainless Cambro',
    status: 'NO_OBVIOUS_VISIBLE_DEFECT',
    destination: 'Asha Community Kitchen',
    pathway: 'Human Food Recovery',
    timestamp: '28 Mins Ago',
    confidence: 96,
  },
  {
    id: 'BATCH-402',
    kitchen: 'Grand Heritage Banquets',
    category: 'Dal Makhani & Paneer Gravy',
    weightKg: 120,
    temp: '61.0°C',
    hoursSinceCooked: 3.0,
    container: 'Sealed Chafing Trays',
    status: 'NO_OBVIOUS_VISIBLE_DEFECT',
    destination: 'Annapurna Seva Shelter',
    pathway: 'Human Food Recovery',
    timestamp: '45 Mins Ago',
    confidence: 94,
  },
  {
    id: 'BATCH-403',
    kitchen: 'City View Convention Center',
    category: 'Assorted Rotis & Naan',
    weightKg: 40,
    temp: '42.0°C',
    hoursSinceCooked: 5.5,
    container: 'Open Food Crates',
    status: 'NEEDS_REVIEW',
    destination: 'Holding Station #2',
    pathway: 'Further Assessment',
    timestamp: '1 Hour Ago',
    confidence: 68,
  },
  {
    id: 'BATCH-404',
    kitchen: 'Silver Spoon Events',
    category: 'Trimmings & Gravy Base',
    weightKg: 110,
    temp: '28.0°C',
    hoursSinceCooked: 8.0,
    container: 'Organic Disposal Bin',
    status: 'VISIBLE_DETERIORATION',
    destination: 'GreenGrove Bio-CNG Plant',
    pathway: 'Organic-Waste Processing',
    timestamp: '2 Hours Ago',
    confidence: 98,
  },
  {
    id: 'BATCH-405',
    kitchen: 'Royal Orchid Pavilion',
    category: 'Vegetable Pulao & Raita',
    weightKg: 95,
    temp: '64.2°C',
    hoursSinceCooked: 2.0,
    container: 'Insulated Cambro',
    status: 'NO_OBVIOUS_VISIBLE_DEFECT',
    destination: 'Balaji Child Welfare Home',
    pathway: 'Human Food Recovery',
    timestamp: '3 Hours Ago',
    confidence: 95,
  },
  {
    id: 'BATCH-406',
    kitchen: 'Emerald Garden Banquets',
    category: 'Vegetable Peelings & Rice Crusts',
    weightKg: 80,
    temp: '22.0°C',
    hoursSinceCooked: 10.0,
    container: 'Bio-Vat #4',
    status: 'VISIBLE_DETERIORATION',
    destination: 'Vrindavan Gaushala Care',
    pathway: 'Organic-Waste Processing',
    timestamp: '4 Hours Ago',
    confidence: 99,
  }
];

// Reconciled Impact numbers: Total = 1,250 kg
// 950 delivered + 30 awaiting + 190 compost/biogas + 80 held/rejected = 1,250 kg
const PATHWAY_DATA = [
  { name: 'Delivered to People', value: 950, color: '#059669', share: '76.0%' },
  { name: 'Organic Compost / Biogas', value: 190, color: '#65a30d', share: '15.2%' },
  { name: 'Held / Safety Quarantine', value: 80, color: '#f59e0b', share: '6.4%' },
  { name: 'Approved, Awaiting Transit', value: 30, color: '#3b82f6', share: '2.4%' },
];

const ORGANIC_ROUTING_DATA = [
  { name: 'Bio-CNG Energy Plant', value: 95, color: '#65a30d', share: '50.0%' },
  { name: 'Gaushala Cattle Feed', value: 65, color: '#eab308', share: '34.2%' },
  { name: 'Vermicompost (Khaad)', value: 30, color: '#10b981', share: '15.8%' },
];

const CATEGORY_BAR_DATA = [
  { category: 'Cooked Rice & Grains', kg: 480 },
  { category: 'Lentils, Curries & Dals', kg: 340 },
  { category: 'Flatbreads (Roti/Naan)', kg: 220 },
  { category: 'Desserts & Sweets', kg: 120 },
  { category: 'Raw Produce / Salads', kg: 90 },
];

const TIMELINE_DATA = [
  { week: 'Wk 1', reported: 140, delivered: 110, divertedBio: 20 },
  { week: 'Wk 2', reported: 155, delivered: 120, divertedBio: 25 },
  { week: 'Wk 3', reported: 130, delivered: 102, divertedBio: 18 },
  { week: 'Wk 4', reported: 165, delivered: 128, divertedBio: 24 },
  { week: 'Wk 5', reported: 175, delivered: 135, divertedBio: 28 },
  { week: 'Wk 6', reported: 150, delivered: 116, divertedBio: 22 },
  { week: 'Wk 7', reported: 160, delivered: 124, divertedBio: 25 },
  { week: 'Wk 8', reported: 175, delivered: 115, divertedBio: 28 },
];

const HOW_IT_WORKS_ROLES = {
  Donor: [
    {
      num: 1,
      title: 'Log Banquet Surplus',
      desc: 'Commercial kitchen logs dish name, approximate weight, and cooking timestamp.',
      icon: Utensils,
      img: 'https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=600&q=80',
      alt: 'Chefs preparing banquet trays'
    },
    {
      num: 2,
      title: 'FreshGuard Optical Scan',
      desc: 'Capture camera image and surface temperature probe for AI verification.',
      icon: Camera,
      img: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80',
      alt: 'Nutritious cooked food close-up'
    },
    {
      num: 3,
      title: 'Automated Routing',
      desc: 'System matches verified batches to nearby shelters or organic digesters.',
      icon: Truck,
      img: 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=600&q=80',
      alt: 'Insulated delivery cargo container'
    },
    {
      num: 4,
      title: 'Digital Handshake',
      desc: 'Recipient acknowledges physical temperature and weight intake at doorstep.',
      icon: CheckCircle2,
      img: 'https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&w=600&q=80',
      alt: 'Volunteers receiving meal crates'
    }
  ],
  Assessor: [
    {
      num: 1,
      title: 'Flagged Queue Triage',
      desc: 'Assessors view items where optical confidence is borderline (<80%) or cooling exceeded 3h.',
      icon: AlertTriangle,
      img: 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=600&q=80',
      alt: 'Quality inspector with tablet'
    },
    {
      num: 2,
      title: 'Multi-Sensor Check',
      desc: 'Cross-reference thermal logger telemetry against ambient humidity and container seals.',
      icon: Thermometer,
      img: 'https://images.unsplash.com/photo-1584727638096-042c45049ebe?auto=format&fit=crop&w=600&q=80',
      alt: 'Digital temperature probe calibration'
    },
    {
      num: 3,
      title: 'Fail-Closed Signoff',
      desc: 'Human assessor certifies safe human consumption or mandatory diversion.',
      icon: ShieldCheck,
      img: 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=600&q=80',
      alt: 'Audit report review'
    },
    {
      num: 4,
      title: 'Ledger Archival',
      desc: 'Immutable batch record logged for traceability and donor feedback loops.',
      icon: FileCheck,
      img: 'https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=600&q=80',
      alt: 'Verified ledger dispatch'
    }
  ],
  Recipient: [
    {
      num: 1,
      title: 'Demand Broadcast',
      desc: 'Community kitchens signal daily meal capacity and dietary preferences.',
      icon: Building2,
      img: 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&w=600&q=80',
      alt: 'Community welfare shelter entrance'
    },
    {
      num: 2,
      title: 'Dispatch Notification',
      desc: 'Real-time alert with batch origin, allergen notes, and estimated delivery van ETA.',
      icon: Clock,
      img: 'https://images.unsplash.com/photo-1526367790999-0150786686a2?auto=format&fit=crop&w=600&q=80',
      alt: 'Courier tracking dispatch ETA'
    },
    {
      num: 3,
      title: 'Physical Intake Verify',
      desc: 'Quick barcode scan and instant infrared surface temperature confirmation.',
      icon: CheckCircle2,
      img: 'https://images.unsplash.com/photo-1577962917302-cd874c4e31d2?auto=format&fit=crop&w=600&q=80',
      alt: 'Kitchen staff validating clean meal pans'
    },
    {
      num: 4,
      title: 'Warm Meal Serving',
      desc: 'Wholesome, safe food served to children, daily-wage workers, and elders.',
      icon: HeartHandshake,
      img: 'https://images.unsplash.com/photo-1509099836639-18ba1795216d?auto=format&fit=crop&w=600&q=80',
      alt: 'Warm meal served with dignity'
    }
  ],
  Processor: [
    {
      num: 1,
      title: 'Organic Feed Triage',
      desc: 'Kitchen trimmings and expired batches separated into compost vs livestock feed.',
      icon: Leaf,
      img: 'https://images.unsplash.com/photo-1589923188900-85dae523342b?auto=format&fit=crop&w=600&q=80',
      alt: 'Clean vegetable trimmings'
    },
    {
      num: 2,
      title: 'Bio-CNG Digestion',
      desc: 'High-moisture cooked scraps routed into anaerobic methanation reactors.',
      icon: Flame,
      img: 'https://images.unsplash.com/photo-1532601224476-15c79f2f7a51?auto=format&fit=crop&w=600&q=80',
      alt: 'Renewable biogas plant pipes'
    },
    {
      num: 3,
      title: 'Gaushala Distribution',
      desc: 'Pure vegetarian grains and fodder delivered to animal welfare shelters.',
      icon: Award,
      img: 'https://images.unsplash.com/photo-1546445317-29f4545e9d53?auto=format&fit=crop&w=600&q=80',
      alt: 'Healthy cattle in sheltered gaushala'
    },
    {
      num: 4,
      title: 'Soil Nutrient Return',
      desc: 'Rich organic nitrogen compost (Khaad) returned to urban community gardens.',
      icon: Sparkles,
      img: 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=600&q=80',
      alt: 'Rich dark compost soil for agriculture'
    }
  ]
};

// ==========================================
// COMPONENT: PERSISTENT AMBER DEMO BANNER
// ==========================================
function DemoBanner({ className = '' }) {
  return (
    <div
      role="region"
      aria-label="Demonstration Notice"
      className={`bg-amber-50/95 border border-amber-300 text-amber-900 px-4 py-2.5 rounded-xl flex items-center justify-center gap-2.5 text-xs sm:text-sm font-medium shadow-sm ${className}`}
    >
      <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" aria-hidden="true" />
      <span>
        <strong>Demonstration data — not live operational results.</strong> All figures, kitchens, and inspection telemetry shown are simulated hackathon test models.
      </span>
    </div>
  );
}

// ==========================================
// COMPONENT: CONFIDENCE RADIAL GAUGE
// ==========================================
function SemicircleGauge({ score = 96, status = 'NO_OBVIOUS_VISIBLE_DEFECT' }) {
  const radius = 45;
  const circumference = Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let strokeColor = '#059669'; // Emerald
  if (status === 'NEEDS_REVIEW') strokeColor = '#f59e0b'; // Amber
  if (status === 'VISIBLE_DETERIORATION') strokeColor = '#e11d48'; // Rose

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative w-32 h-18 flex items-end justify-center overflow-hidden">
        <svg viewBox="0 0 110 65" className="w-32 h-20">
          {/* Background Arc */}
          <path
            d="M 10 55 A 45 45 0 0 1 100 55"
            fill="none"
            stroke="#e2e8f0"
            strokeWidth="8"
            strokeLinecap="round"
          />
          {/* Foreground Arc */}
          <path
            d="M 10 55 A 45 45 0 0 1 100 55"
            fill="none"
            stroke={strokeColor}
            strokeWidth="8"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute bottom-1 flex flex-col items-center">
          <span className="text-2xl font-bold font-mono tracking-tight text-slate-900 tabular-nums">
            {score}%
          </span>
          <span className="text-[11px] font-mono uppercase tracking-wider text-slate-500 -mt-0.5">
            Confidence
          </span>
        </div>
      </div>
    </div>
  );
}

// ==========================================
// MAIN COMPONENT: APP
// ==========================================
export default function App() {
  // Navigation & Scroll-spy
  const [activeSection, setActiveSection] = useState('hero');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // User Authentication State
  const [user, setUser] = useState(null); // { name: 'Aditi Sharma', role: 'Recipient', organization: 'Asha Community Kitchen' }
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [authTab, setAuthTab] = useState('login'); // 'login' | 'register'
  const [authEmail, setAuthEmail] = useState('demo@potbhar.internal');
  const [authPassword, setAuthPassword] = useState('demopass123');
  const [authError, setAuthError] = useState('');

  // Modals & Drawers
  const [donorModalOpen, setDonorModalOpen] = useState(false);
  const [recipientModalOpen, setRecipientModalOpen] = useState(false);
  const [dashboardDrawerOpen, setDashboardDrawerOpen] = useState(false);
  const [legalModalContent, setLegalModalContent] = useState(null); // 'terms' | 'privacy'

  // Dashboard Role Switcher
  const [dashboardRole, setDashboardRole] = useState('Donor'); // 'Donor' | 'Recipient' | 'Assessor'

  // Toast Notification System
  const [toasts, setToasts] = useState([]);
  const addToast = (message, type = 'success') => {
    const id = Date.now() + Math.random().toString(36).substring(2, 6);
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  };

  // Section 2: How It Works active role tab
  const [activeRoleTab, setActiveRoleTab] = useState('Donor');

  // Section 3: FreshGuard AI state
  const [freshGuardTab, setFreshGuardTab] = useState('photo'); // 'photo' | 'risk' | 'history'
  const [scanState, setScanState] = useState('idle'); // 'idle' | 'scanning' | 'result'
  const [selectedSampleImage, setSelectedSampleImage] = useState('Vegetable Biryani');
  const [customImagePreview, setCustomImagePreview] = useState(null);
  const [scanResult, setScanResult] = useState({
    status: 'NO_OBVIOUS_VISIBLE_DEFECT',
    visibleQuality: 'High Visual Freshness',
    confidence: 96,
    metrics: {
      steamIntegrity: 'Active Vapor Thermal Core',
      surfaceOxidation: '0.02% (Nominal)',
      containerSeals: 'Cambro Stainless Gasket Verified',
      moistureRetention: 'Optimal Grain Separation'
    }
  });

  // Quality Risk Interactive Form State
  const [riskCategory, setRiskCategory] = useState('Cooked Grain');
  const [riskHours, setRiskHours] = useState(2.5);
  const [riskTemp, setRiskTemp] = useState(64);
  const [riskContainer, setRiskContainer] = useState('Insulated Cambro');

  // Calculated Risk Score & Tier
  const riskCalculation = useMemo(() => {
    let score = 20; // base risk
    // Temperature risk
    if (riskTemp < 60) score += (60 - riskTemp) * 1.5;
    if (riskTemp < 45) score += 20; // danger zone

    // Hours risk
    if (riskHours > 3) score += (riskHours - 3) * 12;

    // Container penalty
    if (riskContainer === 'Open Food Crates') score += 25;
    if (riskContainer === 'Plastic Tub') score += 12;

    // Category risk
    if (riskCategory === 'Gravy/Dairy') score += 15;

    score = Math.min(100, Math.max(5, Math.round(score)));

    let tier = 'LOW';
    let decision = 'Dispatch Approved';
    let colorClass = 'text-emerald-700 bg-emerald-50 border-emerald-300';
    let barColor = 'bg-emerald-500';

    if (score >= 45 && score < 70) {
      tier = 'MEDIUM';
      decision = 'HOLD – Needs Human Assessor';
      colorClass = 'text-amber-700 bg-amber-50 border-amber-300';
      barColor = 'bg-amber-500';
    } else if (score >= 70) {
      tier = 'HIGH';
      decision = 'REJECTED FOR HUMANS – Divert to Gaushala/Bio-CNG';
      colorClass = 'text-rose-700 bg-rose-50 border-rose-300';
      barColor = 'bg-rose-500';
    }

    return { score, tier, decision, colorClass, barColor };
  }, [riskCategory, riskHours, riskTemp, riskContainer]);

  // Section 5: Impact Analytics Tab
  const [impactTab, setImpactTab] = useState('overview'); // 'overview' | 'pathways' | 'timeline'
  const [timelineFilter, setTimelineFilter] = useState('ALL');

  // Batches master state (for interactions)
  const [batches, setBatches] = useState(SAMPLE_BATCHES_INITIAL);

  // New Surplus Form State (Donor Modal)
  const [donorStep, setDonorStep] = useState(1);
  const [newSurplus, setNewSurplus] = useState({
    foodName: 'Kashmiri Pulao & Kofta Curry',
    category: 'Cooked Grain',
    weightKg: 65,
    hoursCooked: 2.0,
    temp: 65,
    container: 'Insulated Cambro',
    kitchen: 'Saffron Hall Caterers'
  });

  // Recipient search query
  const [recipientSearch, setRecipientSearch] = useState('');
  const [recipientCategoryFilter, setRecipientCategoryFilter] = useState('ALL');

  // Keyboard accessibility: Escape closes any open modal
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        setAuthModalOpen(false);
        setDonorModalOpen(false);
        setRecipientModalOpen(false);
        setDashboardDrawerOpen(false);
        setLegalModalContent(null);
        setMobileMenuOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Lock body scroll when any modal or drawer is active
  useEffect(() => {
    const isModalOpen =
      authModalOpen ||
      donorModalOpen ||
      recipientModalOpen ||
      dashboardDrawerOpen ||
      legalModalContent !== null;
    document.body.style.overflow = isModalOpen ? 'hidden' : 'unset';
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [authModalOpen, donorModalOpen, recipientModalOpen, dashboardDrawerOpen, legalModalContent]);

  // Scrollspy observer for active section
  useEffect(() => {
    const sections = ['hero', 'how-it-works', 'freshguard', 'organic-routing', 'impact'];
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id);
          }
        });
      },
      { threshold: 0.3 }
    );

    sections.forEach((id) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  // FreshGuard Simulated Scan Trigger
  const handleRunAnalysis = () => {
    setScanState('scanning');
    setTimeout(() => {
      if (selectedSampleImage === 'Mixed Curry (Aged)') {
        setScanResult({
          status: 'VISIBLE_DETERIORATION',
          visibleQuality: 'Surface Separation & Degradation',
          confidence: 97,
          metrics: {
            steamIntegrity: 'No Active Thermal Vapor',
            surfaceOxidation: '28.4% (Critical Surface Film)',
            containerSeals: 'Open Air Exposure (>4h)',
            moistureRetention: 'Phase Separation Observed'
          }
        });
      } else if (selectedSampleImage === 'Dal & Rice Tray') {
        setScanResult({
          status: 'NEEDS_REVIEW',
          visibleQuality: 'Borderline Temperature Gradient',
          confidence: 74,
          metrics: {
            steamIntegrity: 'Weak Vapor Formation',
            surfaceOxidation: '6.1% (Mild Edge Crusting)',
            containerSeals: 'Partial Steel Cover',
            moistureRetention: 'Acceptable Moisture Balance'
          }
        });
      } else {
        setScanResult({
          status: 'NO_OBVIOUS_VISIBLE_DEFECT',
          visibleQuality: 'High Visual Freshness & Thermal Steam',
          confidence: 96,
          metrics: {
            steamIntegrity: 'Active Vapor Thermal Core',
            surfaceOxidation: '0.02% (Nominal)',
            containerSeals: 'Cambro Stainless Gasket Verified',
            moistureRetention: 'Optimal Grain Separation'
          }
        });
      }
      setScanState('result');
      addToast('Optical analysis completed. Sensor data evaluated.');
    }, 1500);
  };

  // Submit scan result for formal human assessor review
  const handleSubmitFormalReview = () => {
    const newBatch = {
      id: `BATCH-${Math.floor(400 + Math.random() * 500)}`,
      kitchen: user ? user.organization : 'Saffron Hall Caterers',
      category: selectedSampleImage,
      weightKg: 55,
      temp: scanResult.status === 'VISIBLE_DETERIORATION' ? '28.0°C' : '63.0°C',
      hoursSinceCooked: scanResult.status === 'VISIBLE_DETERIORATION' ? 6.0 : 2.0,
      container: 'Insulated Cambro',
      status: scanResult.status,
      destination:
        scanResult.status === 'VISIBLE_DETERIORATION'
          ? 'GreenGrove Bio-CNG Plant'
          : scanResult.status === 'NEEDS_REVIEW'
          ? 'Holding Station #1'
          : 'Asha Community Kitchen',
      pathway:
        scanResult.status === 'VISIBLE_DETERIORATION'
          ? 'Organic-Waste Processing'
          : scanResult.status === 'NEEDS_REVIEW'
          ? 'Further Assessment'
          : 'Human Food Recovery',
      timestamp: 'Just Now',
      confidence: scanResult.confidence
    };
    setBatches((prev) => [newBatch, ...prev]);
    addToast(
      scanResult.status === 'NO_OBVIOUS_VISIBLE_DEFECT'
        ? 'Batch queued for dispatch to community partner.'
        : 'Batch submitted for formal human assessor review.'
    );
    setFreshGuardTab('history');
  };

  // Donor report surplus submission handler
  const handleDonorSubmit = (e) => {
    e.preventDefault();
    const createdBatch = {
      id: `BATCH-${Math.floor(400 + Math.random() * 500)}`,
      kitchen: newSurplus.kitchen,
      category: `${newSurplus.foodName} (${newSurplus.category})`,
      weightKg: Number(newSurplus.weightKg),
      temp: `${newSurplus.temp}°C`,
      hoursSinceCooked: Number(newSurplus.hoursCooked),
      container: newSurplus.container,
      status: Number(newSurplus.temp) >= 60 ? 'NO_OBVIOUS_VISIBLE_DEFECT' : 'NEEDS_REVIEW',
      destination: Number(newSurplus.temp) >= 60 ? 'Asha Community Kitchen' : 'Holding Station #2',
      pathway: Number(newSurplus.temp) >= 60 ? 'Human Food Recovery' : 'Further Assessment',
      timestamp: 'Just Now',
      confidence: 94
    };
    setBatches((prev) => [createdBatch, ...prev]);
    setDonorModalOpen(false);
    setDonorStep(1);
    addToast(`Surplus food report logged! ${createdBatch.weightKg} kg added to dispatch radar.`);
  };

  // Recipient accept batch handler
  const handleAcceptBatch = (batchId) => {
    setBatches((prev) =>
      prev.map((b) =>
        b.id === batchId
          ? { ...b, destination: user ? user.organization : 'Asha Community Kitchen', status: 'ACCEPTED_BY_RECIPIENT' }
          : b
      )
    );
    addToast(`Batch ${batchId} accepted! Allocation confirmed for community delivery.`);
    setRecipientModalOpen(false);
  };

  // Assessor decision handler in dashboard
  const handleAssessorDecision = (batchId, approve) => {
    setBatches((prev) =>
      prev.map((b) => {
        if (b.id === batchId) {
          return {
            ...b,
            status: approve ? 'NO_OBVIOUS_VISIBLE_DEFECT' : 'VISIBLE_DETERIORATION',
            pathway: approve ? 'Human Food Recovery' : 'Organic-Waste Processing',
            destination: approve ? 'Asha Community Kitchen' : 'GreenGrove Bio-CNG Plant'
          };
        }
        return b;
      })
    );
    addToast(
      approve
        ? `Batch ${batchId} certified and released to food recovery route.`
        : `Batch ${batchId} diverted to organic digestion and cattle feed.`
    );
  };

  // Quick demo login helper
  const handleDemoLogin = (role = 'Donor') => {
    if (role === 'Donor') {
      setUser({
        name: 'Rahul Verma',
        role: 'Donor',
        organization: 'Saffron Hall Caterers',
        email: 'rahul@saffronhall.internal'
      });
      setDashboardRole('Donor');
    } else if (role === 'Recipient') {
      setUser({
        name: 'Aditi Sharma',
        role: 'Recipient',
        organization: 'Asha Community Kitchen',
        email: 'aditi@ashakitchen.internal'
      });
      setDashboardRole('Recipient');
    } else {
      setUser({
        name: 'Priya Nambiar',
        role: 'Assessor',
        organization: 'City Quality Assessor Unit',
        email: 'priya@assessor.internal'
      });
      setDashboardRole('Assessor');
    }
    setAuthModalOpen(false);
    addToast(`Welcome back, ${role === 'Donor' ? 'Rahul' : role === 'Recipient' ? 'Aditi' : 'Priya'}! Demo session active.`);
  };

  // Filtered batches for Recipient Modal
  const filteredRecipientBatches = useMemo(() => {
    return batches.filter((b) => {
      const matchesSearch =
        b.category.toLowerCase().includes(recipientSearch.toLowerCase()) ||
        b.kitchen.toLowerCase().includes(recipientSearch.toLowerCase());
      const matchesCat =
        recipientCategoryFilter === 'ALL' ||
        (recipientCategoryFilter === 'HUMAN' && b.pathway === 'Human Food Recovery') ||
        (recipientCategoryFilter === 'GRAIN' && b.category.includes('Grain')) ||
        (recipientCategoryFilter === 'CURRY' && (b.category.includes('Gravy') || b.category.includes('Dal')));
      return matchesSearch && matchesCat && b.status !== 'VISIBLE_DETERIORATION';
    });
  }, [batches, recipientSearch, recipientCategoryFilter]);

  // Filtered batches for Timeline table
  const filteredTimelineBatches = useMemo(() => {
    if (timelineFilter === 'ALL') return batches;
    if (timelineFilter === 'DELIVERED') return batches.filter((b) => b.pathway === 'Human Food Recovery');
    if (timelineFilter === 'ORGANIC') return batches.filter((b) => b.pathway === 'Organic-Waste Processing');
    if (timelineFilter === 'HOLD') return batches.filter((b) => b.pathway === 'Further Assessment');
    return batches;
  }, [batches, timelineFilter]);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans selection:bg-emerald-100 selection:text-emerald-900">
      {/* ==========================================
          TOAST NOTIFICATION REGION
      ========================================== */}
      <div
        role="status"
        aria-live="polite"
        className="fixed bottom-5 right-5 z-50 flex flex-col gap-2.5 max-w-sm pointer-events-none"
      >
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`pointer-events-auto p-4 rounded-2xl shadow-xl border flex items-start gap-3 backdrop-blur-md bg-white/95 transition-all duration-300 animate-slide-up ${
              toast.type === 'error'
                ? 'border-rose-200 text-rose-950'
                : toast.type === 'warning'
                ? 'border-amber-200 text-amber-950'
                : 'border-emerald-200 text-emerald-950'
            }`}
          >
            {toast.type === 'error' ? (
              <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
            ) : toast.type === 'warning' ? (
              <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            ) : (
              <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
            )}
            <div className="flex-1">
              <p className="text-sm font-semibold leading-snug">{toast.message}</p>
            </div>
            <button
              onClick={() => setToasts((prev) => prev.filter((t) => t.id !== toast.id))}
              className="text-slate-400 hover:text-slate-700 transition-colors p-1"
              aria-label="Close notification"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        ))}
      </div>

      {/* ==========================================
          HEADER / NAVBAR
      ========================================== */}
      <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200 transition-colors">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            {/* Logo & Brand Wordmark */}
            <a
              href="#hero"
              className="flex items-center gap-3 group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 rounded-xl p-1"
            >
              <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-emerald-600 to-emerald-700 flex items-center justify-center text-white shadow-md shadow-emerald-600/20 group-hover:scale-105 transition-transform duration-200">
                <Leaf className="w-6 h-6 transform -rotate-12" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-outfit font-extrabold text-2xl tracking-tight text-slate-900 group-hover:text-emerald-700 transition-colors">
                    POTBHAR
                  </span>
                  <span className="text-[11px] font-mono uppercase bg-amber-100 text-amber-800 font-semibold px-2 py-0.5 rounded-full border border-amber-300">
                    Prototype
                  </span>
                </div>
                <p className="text-xs text-slate-500 font-medium hidden sm:block">
                  Har Pet Bhare, Har Nivala Sambhale
                </p>
              </div>
            </a>

            {/* Desktop Navigation Links (with scroll-spy indicator) */}
            <nav className="hidden md:flex items-center gap-1 lg:gap-2" aria-label="Main Navigation">
              {[
                { id: 'hero', label: 'Home' },
                { id: 'how-it-works', label: 'How It Works' },
                { id: 'freshguard', label: 'FreshGuard AI' },
                { id: 'organic-routing', label: 'Organic Routing' },
                { id: 'impact', label: 'Impact' },
              ].map((link) => {
                const isActive = activeSection === link.id;
                return (
                  <a
                    key={link.id}
                    href={`#${link.id}`}
                    className={`relative px-3.5 py-2 rounded-xl text-sm font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 ${
                      isActive
                        ? 'text-emerald-700 bg-emerald-50'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
                    }`}
                  >
                    {link.label}
                    {isActive && (
                      <span className="absolute bottom-0 left-3 right-3 h-0.5 bg-emerald-600 rounded-full" />
                    )}
                  </a>
                );
              })}
            </nav>

            {/* Auth & Role Dashboard Controls */}
            <div className="flex items-center gap-3">
              {user ? (
                <div className="flex items-center gap-2.5">
                  <button
                    onClick={() => setDashboardDrawerOpen(true)}
                    className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-sm font-semibold border border-slate-300 transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
                  >
                    <User className="w-4 h-4 text-emerald-600" />
                    <span className="hidden sm:inline">{user.name}</span>
                    <span className="text-xs bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded">
                      {user.role}
                    </span>
                  </button>
                  <button
                    onClick={() => {
                      setUser(null);
                      addToast('Logged out of demo session.');
                    }}
                    className="text-xs text-slate-500 hover:text-slate-900 underline px-2 py-1"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setAuthModalOpen(true)}
                  className="px-4 py-2 rounded-xl text-sm font-semibold text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
                >
                  Log in
                </button>
              )}

              <button
                onClick={() => setDashboardDrawerOpen(true)}
                className="hidden sm:flex items-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 text-white text-sm font-bold shadow-sm shadow-emerald-600/25 transition-all duration-200 hover:-translate-y-0.5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
              >
                <Layers className="w-4 h-4" />
                <span>Dashboard</span>
              </button>

              {/* Mobile Menu Button */}
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden p-2.5 rounded-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
                aria-label="Toggle Navigation Menu"
                aria-expanded={mobileMenuOpen}
              >
                {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Slide-down Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-slate-200 bg-white/95 backdrop-blur-md px-4 py-5 shadow-lg animate-fade-in">
            <nav className="flex flex-col gap-2">
              {[
                { id: 'hero', label: 'Home' },
                { id: 'how-it-works', label: 'How It Works' },
                { id: 'freshguard', label: 'FreshGuard AI' },
                { id: 'organic-routing', label: 'Organic Routing' },
                { id: 'impact', label: 'Impact' },
              ].map((link) => (
                <a
                  key={link.id}
                  href={`#${link.id}`}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`px-4 py-3 rounded-xl text-base font-semibold transition-colors ${
                    activeSection === link.id
                      ? 'bg-emerald-50 text-emerald-700'
                      : 'text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  {link.label}
                </a>
              ))}
              <div className="pt-3 border-t border-slate-200 flex flex-col gap-2">
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    setDashboardDrawerOpen(true);
                  }}
                  className="w-full py-3 rounded-xl bg-emerald-600 text-white font-bold text-center shadow-sm"
                >
                  Open Role Dashboard
                </button>
                {!user && (
                  <button
                    onClick={() => {
                      setMobileMenuOpen(false);
                      setAuthModalOpen(true);
                    }}
                    className="w-full py-2.5 rounded-xl border border-slate-300 text-slate-700 font-semibold text-center"
                  >
                    Log In / Demo User
                  </button>
                )}
              </div>
            </nav>
          </div>
        )}
      </header>

      {/* Main Content Sections */}
      <main className="flex-1">
        {/* ==========================================
            SECTION 1: HERO
        ========================================== */}
        <section id="hero" className="relative py-14 sm:py-20 overflow-hidden bg-slate-50">
          {/* Subtle Ambient Radial Gradients */}
          <div
            className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-gradient-to-b from-emerald-100/50 via-amber-50/40 to-transparent pointer-events-none rounded-full blur-3xl -z-10"
            aria-hidden="true"
          />

          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
              {/* Left Column: Copy & Actions */}
              <div className="lg:col-span-7 flex flex-col items-start text-left">
                {/* Eyebrow Pill */}
                <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-100/80 border border-emerald-300 text-emerald-800 text-xs uppercase tracking-wider font-semibold mb-6 shadow-sm">
                  <Sparkles className="w-3.5 h-3.5 text-emerald-700" />
                  <span>POTBHAR HACKATHON PROTOTYPE · ZERO-WASTE DISPATCH</span>
                </div>

                {/* Single H1 with curved amber SVG accent */}
                <h1 className="font-outfit text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-900 leading-[1.08] mb-6">
                  From Surplus to Sustenance.{' '}
                  <span className="relative inline-block text-amber-600">
                    From Waste to Worth.
                    <svg
                      className="absolute -bottom-2 left-0 w-full h-3 text-amber-400"
                      viewBox="0 0 250 12"
                      fill="none"
                      preserveAspectRatio="none"
                      aria-hidden="true"
                    >
                      <path
                        d="M3 9C55 3 195 2 247 9"
                        stroke="currentColor"
                        strokeWidth="4"
                        strokeLinecap="round"
                      />
                    </svg>
                  </span>
                </h1>

                {/* Subcopy */}
                <p className="text-base sm:text-lg text-slate-600 max-w-2xl leading-relaxed mb-8">
                  POTBHAR coordinates surplus banquet meals, optical food-safety verification, community distribution, and organic waste routing—ensuring every morsel nourishes people or returns fertility to the earth.
                </p>

                {/* Dual Primary CTAs */}
                <div className="flex flex-wrap items-center gap-4 w-full sm:w-auto mb-10">
                  <button
                    onClick={() => setDonorModalOpen(true)}
                    className="w-full sm:w-auto px-7 py-4 rounded-2xl bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 text-white font-bold text-base shadow-lg shadow-emerald-600/30 transition-all duration-200 hover:-translate-y-0.5 flex items-center justify-center gap-2.5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
                  >
                    <Utensils className="w-5 h-5" />
                    <span>Report Surplus Food</span>
                    <ChevronRight className="w-4 h-4 ml-0.5" />
                  </button>

                  <button
                    onClick={() => setRecipientModalOpen(true)}
                    className="w-full sm:w-auto px-7 py-4 rounded-2xl bg-white hover:bg-slate-100 text-slate-800 border-2 border-slate-300 font-bold text-base shadow-sm transition-all duration-200 hover:-translate-y-0.5 flex items-center justify-center gap-2.5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
                  >
                    <HeartHandshake className="w-5 h-5 text-emerald-600" />
                    <span>Find Food Donations</span>
                  </button>
                </div>

                {/* Trust Strip (3 Mini Stats) */}
                <div className="w-full pt-8 border-t border-slate-200/80 grid grid-cols-3 gap-4">
                  <div>
                    <div className="font-outfit text-2xl sm:text-3xl font-extrabold text-slate-900 tabular-nums">
                      1,250 <span className="text-sm font-semibold text-slate-500">kg</span>
                    </div>
                    <div className="text-xs text-slate-500 font-medium mt-0.5">
                      Managed (Sample Data)
                    </div>
                  </div>
                  <div>
                    <div className="font-outfit text-2xl sm:text-3xl font-extrabold text-emerald-700 tabular-nums">
                      2,375
                    </div>
                    <div className="text-xs text-slate-500 font-medium mt-0.5">
                      Estimated Meals (Demo)
                    </div>
                  </div>
                  <div>
                    <div className="font-outfit text-2xl sm:text-3xl font-extrabold text-amber-600 tabular-nums">
                      100%
                    </div>
                    <div className="text-xs text-slate-500 font-medium mt-0.5">
                      Landfill Diversion
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Column: Hero Visual with Rotated Frame & Floating Glass Cards */}
              <div className="lg:col-span-5 relative flex justify-center">
                {/* Rotated Gradient Backdrop Frame */}
                <div
                  className="absolute inset-2 sm:inset-4 rounded-3xl bg-gradient-to-tr from-emerald-500/20 via-amber-400/20 to-emerald-600/30 rotate-3 transform -z-10 blur-xs transition-transform hover:rotate-2 duration-500"
                  aria-hidden="true"
                />

                <div className="relative w-full max-w-md aspect-[4/3] sm:aspect-[4/3] rounded-3xl overflow-hidden shadow-2xl border-4 border-white bg-gradient-to-br from-emerald-700 to-amber-600">
                  <img
                    src="https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&w=1000&q=80"
                    alt="Volunteers packing warm community meals with care and hygiene"
                    loading="lazy"
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.currentTarget.style.display = 'none';
                    }}
                  />

                  {/* Gradient Overlay for card readability */}
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-950/60 via-transparent to-black/20" />

                  {/* Floating Glass Card 1 (Top-Right): Approved Batch */}
                  <div className="absolute top-4 right-4 sm:top-6 sm:right-6 bg-white/90 backdrop-blur-md border border-white/80 p-3 sm:p-3.5 rounded-2xl shadow-xl flex items-center gap-3 animate-fade-in max-w-[240px]">
                    <div className="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-700 shrink-0">
                      <CheckCircle2 className="w-5 h-5" />
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center gap-1.5">
                        <span className="text-xs font-mono font-bold text-slate-900">#A-102</span>
                        <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-100 text-emerald-800">
                          Approved
                        </span>
                      </div>
                      <p className="text-xs text-slate-600 truncate mt-0.5">
                        64°C Paneer Biryani · Asha Kitchen
                      </p>
                    </div>
                  </div>

                  {/* Floating Glass Card 2 (Bottom-Left): Organic Compost Confirmation */}
                  <div className="absolute bottom-4 left-4 sm:bottom-6 sm:left-6 bg-white/90 backdrop-blur-md border border-white/80 p-3 sm:p-3.5 rounded-2xl shadow-xl flex items-center gap-3 animate-fade-in max-w-[240px]">
                    <div className="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center text-amber-700 shrink-0">
                      <Leaf className="w-5 h-5" />
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center gap-1.5">
                        <span className="text-xs font-mono font-bold text-slate-900">Route #C-04</span>
                        <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-amber-100 text-amber-800">
                          Confirmed
                        </span>
                      </div>
                      <p className="text-xs text-slate-600 truncate mt-0.5">
                        190 kg trimmings → Bio-CNG & Khaad
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ==========================================
            SECTION 2: HOW IT WORKS (TABBED BY ROLE)
        ========================================== */}
        <section id="how-it-works" className="py-14 sm:py-20 bg-white border-y border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Section Header */}
            <div className="text-center max-w-3xl mx-auto mb-10">
              <span className="text-xs uppercase tracking-wider font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full">
                Interactive Dispatch Protocols
              </span>
              <h2 className="font-outfit text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight mt-3 mb-4">
                How POTBHAR Coordinates Every Meal
              </h2>
              <p className="text-base text-slate-600">
                Explore the workflow tailored to each stakeholder. From commercial banquet halls to quality assessors and circular processors.
              </p>
            </div>

            {/* Persistent Demonstration Notice */}
            <DemoBanner className="mb-10 max-w-2xl mx-auto" />

            {/* Role Tabs */}
            <div className="flex justify-center mb-12">
              <div className="inline-flex p-1.5 rounded-2xl bg-slate-100 border border-slate-200 shadow-inner max-w-full overflow-x-auto">
                {['Donor', 'Assessor', 'Recipient', 'Processor'].map((role) => {
                  const isSelected = activeRoleTab === role;
                  return (
                    <button
                      key={role}
                      onClick={() => setActiveRoleTab(role)}
                      className={`px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 ${
                        isSelected
                          ? 'bg-white text-emerald-800 shadow-md border border-slate-200/80 scale-[1.02]'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      {role === 'Donor' && '1. Donor Kitchen'}
                      {role === 'Assessor' && '2. Quality Assessor'}
                      {role === 'Recipient' && '3. Recipient Shelter'}
                      {role === 'Processor' && '4. Organic Processor'}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Horizontal 4-Step Stepper (Vertical on mobile) */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 items-stretch mb-16">
              {HOW_IT_WORKS_ROLES[activeRoleTab].map((step, idx) => {
                const StepIcon = step.icon;
                return (
                  <div
                    key={step.num}
                    className="potbhar-card p-6 h-full flex flex-col justify-between relative group"
                  >
                    <div>
                      {/* Step Number & Connector indicator */}
                      <div className="flex items-center justify-between mb-4">
                        <div className="w-10 h-10 rounded-2xl bg-emerald-50 text-emerald-700 border border-emerald-200 font-outfit font-extrabold flex items-center justify-center text-lg shadow-xs group-hover:bg-emerald-600 group-hover:text-white transition-colors duration-200">
                          {step.num}
                        </div>
                        <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center text-slate-500">
                          <StepIcon className="w-5 h-5" />
                        </div>
                      </div>

                      {/* Step Image */}
                      <div className="w-full aspect-[4/3] rounded-xl overflow-hidden mb-4 bg-slate-100 border border-slate-200">
                        <img
                          src={step.img}
                          alt={step.alt}
                          loading="lazy"
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                          onError={(e) => {
                            e.currentTarget.style.display = 'none';
                          }}
                        />
                      </div>

                      <h3 className="font-outfit font-bold text-lg text-slate-900 mb-2">
                        {step.title}
                      </h3>
                      <p className="text-sm text-slate-600 leading-relaxed">
                        {step.desc}
                      </p>
                    </div>

                    <div className="mt-6 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400 font-medium">
                      <span>Step {step.num} of 4</span>
                      <span className="font-mono text-emerald-600 font-semibold">Active Model</span>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* 4 Equal-Height Pathway Cards */}
            <div className="mt-8">
              <div className="text-center mb-8">
                <h3 className="font-outfit text-2xl font-bold text-slate-900">
                  Four Reconciled Dispatch Pathways
                </h3>
                <p className="text-sm text-slate-600 mt-1">
                  Guaranteed safe routing: human food recovery takes priority, while all scraps avoid landfills.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 items-stretch">
                {/* Pathway 1 */}
                <div className="potbhar-card p-6 h-full flex flex-col border-t-4 border-t-emerald-600">
                  <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-700 flex items-center justify-center mb-4">
                    <HeartHandshake className="w-6 h-6" />
                  </div>
                  <h4 className="font-outfit font-bold text-lg text-slate-900 mb-2">
                    Human-Food Recovery
                  </h4>
                  <p className="text-sm text-slate-600 leading-relaxed mb-6">
                    Freshly prepared banquet surplus with verified core temperature (&gt;60°C) delivered directly to shelter kitchens within 90 minutes.
                  </p>
                  <div className="mt-auto pt-4 border-t border-slate-100 flex items-center justify-between">
                    <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                      Tier 1 · Priority
                    </span>
                    <span className="text-xs font-mono text-slate-500 font-medium">950 kg logged</span>
                  </div>
                </div>

                {/* Pathway 2 */}
                <div className="potbhar-card p-6 h-full flex flex-col border-t-4 border-t-amber-500">
                  <div className="w-12 h-12 rounded-2xl bg-amber-50 text-amber-700 flex items-center justify-center mb-4">
                    <AlertTriangle className="w-6 h-6" />
                  </div>
                  <h4 className="font-outfit font-bold text-lg text-slate-900 mb-2">
                    Further Assessment
                  </h4>
                  <p className="text-sm text-slate-600 leading-relaxed mb-6">
                    Fail-closed safety quarantine. Dishes with uncertain camera readings or cooling lag held for certified human inspector sign-off.
                  </p>
                  <div className="mt-auto pt-4 border-t border-slate-100 flex items-center justify-between">
                    <span className="text-xs font-bold text-amber-700 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-200">
                      Tier 2 · Holding
                    </span>
                    <span className="text-xs font-mono text-slate-500 font-medium">80 kg checked</span>
                  </div>
                </div>

                {/* Pathway 3 */}
                <div className="potbhar-card p-6 h-full flex flex-col border-t-4 border-t-lime-600">
                  <div className="w-12 h-12 rounded-2xl bg-lime-50 text-lime-700 flex items-center justify-center mb-4">
                    <Leaf className="w-6 h-6" />
                  </div>
                  <h4 className="font-outfit font-bold text-lg text-slate-900 mb-2">
                    Organic-Waste Processing
                  </h4>
                  <p className="text-sm text-slate-600 leading-relaxed mb-6">
                    Non-edible peelings and aged gravies channeled to certified Gaushala cattle shelters, anaerobic Bio-CNG, and organic vermicompost.
                  </p>
                  <div className="mt-auto pt-4 border-t border-slate-100 flex items-center justify-between">
                    <span className="text-xs font-bold text-lime-700 bg-lime-50 px-2.5 py-1 rounded-full border border-lime-200">
                      Tier 3 · Circular
                    </span>
                    <span className="text-xs font-mono text-slate-500 font-medium">190 kg diverted</span>
                  </div>
                </div>

                {/* Pathway 4 */}
                <div className="potbhar-card p-6 h-full flex flex-col border-t-4 border-t-blue-600">
                  <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-700 flex items-center justify-center mb-4">
                    <TrendingUp className="w-6 h-6" />
                  </div>
                  <h4 className="font-outfit font-bold text-lg text-slate-900 mb-2">
                    Waste Prevention
                  </h4>
                  <p className="text-sm text-slate-600 leading-relaxed mb-6">
                    Algorithmic feedback telemetry returned to commercial banquet managers to optimize headcounts and reduce recurring batch overproduction.
                  </p>
                  <div className="mt-auto pt-4 border-t border-slate-100 flex items-center justify-between">
                    <span className="text-xs font-bold text-blue-700 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200">
                      Tier 4 · Source
                    </span>
                    <span className="text-xs font-mono text-slate-500 font-medium">Insights Engine</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ==========================================
            SECTION 3: FRESHGUARD AI (SCANNER & RISK)
        ========================================== */}
        <section id="freshguard" className="py-14 sm:py-20 bg-slate-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
              {/* Left Column: Context, Safeguards & Warning */}
              <div className="lg:col-span-5 flex flex-col justify-between">
                <div>
                  <span className="text-xs uppercase tracking-wider font-semibold text-emerald-800 bg-emerald-100 border border-emerald-300 px-3 py-1 rounded-full">
                    Computer Vision & Sensor Telemetry
                  </span>
                  <h2 className="font-outfit text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight mt-3 mb-4">
                    FreshGuard AI: Supporting Evidence Layer
                  </h2>
                  <p className="text-base text-slate-600 leading-relaxed mb-6">
                    FreshGuard evaluates optical food surface integrity, thermal core steam, and elapsed holding duration to recommend recovery routing.
                  </p>

                  {/* Bullet Checklist of Capabilities */}
                  <div className="space-y-3.5 mb-8">
                    {[
                      {
                        title: 'Optical Defect & Surface Moisture',
                        desc: 'Identifies visible oxidation, separation, or crusting.'
                      },
                      {
                        title: 'Elapsed Thermal Decay Curve',
                        desc: 'Cross-verifies kitchen cooking time against digital probe temp.'
                      },
                      {
                        title: 'Container & Gasket Classification',
                        desc: 'Checks seal integrity of cambros and chafing dishes.'
                      },
                      {
                        title: 'Mandatory Fail-Closed Architecture',
                        desc: 'Uncertain signals automatically divert to human inspection.'
                      }
                    ].map((item, idx) => (
                      <div key={idx} className="flex items-start gap-3">
                        <div className="w-6 h-6 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0 mt-0.5">
                          <Check className="w-3.5 h-3.5 stroke-[3]" />
                        </div>
                        <div>
                          <h4 className="text-sm font-bold text-slate-900">{item.title}</h4>
                          <p className="text-xs text-slate-500 leading-normal">{item.desc}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Mandatory Warning Box inside Section */}
                <div className="p-4 rounded-2xl bg-amber-50/90 border border-amber-300 text-amber-950 text-xs leading-relaxed flex items-start gap-3 shadow-xs">
                  <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <strong className="font-semibold block mb-0.5 text-amber-900">
                      FreshGuard output is supporting evidence, not a food-safety certificate.
                    </strong>
                    Uncertain predictions fail closed: our dispatch rule mandates{' '}
                    <span className="font-mono font-bold bg-amber-200/60 px-1 py-0.5 rounded text-amber-900">
                      HOLD – needs human assessor
                    </span>
                    . We never label uncertain batches as safe.
                  </div>
                </div>
              </div>

              {/* Right Column: Interactive Scanner Card with 3 Tabs */}
              <div className="lg:col-span-7">
                <div className="potbhar-card p-6 sm:p-8 bg-white border border-slate-200 shadow-lg rounded-3xl">
                  {/* Scanner Tabs Header */}
                  <div className="flex items-center justify-between pb-4 border-b border-slate-200 mb-6 flex-wrap gap-2">
                    <div className="flex items-center gap-1.5 p-1 bg-slate-100 rounded-xl border border-slate-200">
                      {[
                        { id: 'photo', label: 'Photo Analysis' },
                        { id: 'risk', label: 'Quality Risk' },
                        { id: 'history', label: `History (${batches.length})` }
                      ].map((tab) => (
                        <button
                          key={tab.id}
                          onClick={() => setFreshGuardTab(tab.id)}
                          className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                            freshGuardTab === tab.id
                              ? 'bg-white text-emerald-800 shadow-sm border border-slate-200'
                              : 'text-slate-600 hover:text-slate-900'
                          }`}
                        >
                          {tab.label}
                        </button>
                      ))}
                    </div>

                    <span className="text-[11px] font-mono text-slate-400 bg-slate-50 border border-slate-200 px-2 py-1 rounded">
                      Model v2.4-Hackathon
                    </span>
                  </div>

                  {/* TAB 1: PHOTO ANALYSIS */}
                  {freshGuardTab === 'photo' && (
                    <div>
                      {/* Sample Selection Chips */}
                      <div className="mb-4">
                        <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">
                          Select Demonstration Sample Dish:
                        </label>
                        <div className="flex flex-wrap gap-2">
                          {[
                            'Vegetable Biryani',
                            'Dal & Rice Tray',
                            'Mixed Curry (Aged)'
                          ].map((chip) => (
                            <button
                              key={chip}
                              onClick={() => {
                                setSelectedSampleImage(chip);
                                setScanState('idle');
                              }}
                              className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all ${
                                selectedSampleImage === chip
                                  ? 'bg-emerald-50 text-emerald-800 border-emerald-300 font-bold shadow-xs'
                                  : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                              }`}
                            >
                              {chip}
                              {chip === 'Mixed Curry (Aged)' && ' (Degraded)'}
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Photo Dropzone / Preview Area */}
                      <div className="relative aspect-video rounded-2xl overflow-hidden bg-slate-900 border-2 border-dashed border-slate-300 flex items-center justify-center mb-6 group">
                        {/* Sample Image Background */}
                        <img
                          src={
                            selectedSampleImage === 'Mixed Curry (Aged)'
                              ? 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80'
                              : selectedSampleImage === 'Dal & Rice Tray'
                              ? 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=800&q=80'
                              : 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=80'
                          }
                          alt={selectedSampleImage}
                          className={`w-full h-full object-cover transition-opacity duration-300 ${
                            scanState === 'scanning' ? 'opacity-40 filter blur-xs' : 'opacity-85'
                          }`}
                        />

                        {/* Scanner Laser Sweep Line Animation */}
                        {scanState === 'scanning' && (
                          <div className="absolute inset-0 pointer-events-none flex flex-col justify-start">
                            <div className="w-full h-1 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_15px_#10b981] animate-laser-sweep" />
                            <div className="absolute inset-0 flex flex-col items-center justify-center text-white bg-slate-950/40 backdrop-blur-xs">
                              <RotateCcw className="w-8 h-8 text-emerald-400 animate-spin mb-2" />
                              <span className="font-mono text-sm tracking-wider font-bold">
                                EVALUATING SPECTRAL DENSITY...
                              </span>
                              <span className="font-mono text-xs text-slate-300 mt-1">
                                Checking surface lipid separation & steam
                              </span>
                            </div>
                          </div>
                        )}

                        {/* Idle Overlay Prompt */}
                        {scanState === 'idle' && (
                          <div className="absolute inset-0 bg-slate-950/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                            <span className="bg-white/90 backdrop-blur-md text-slate-900 text-xs font-semibold px-3 py-1.5 rounded-full shadow-md">
                              Click Analyse below to run optical scan
                            </span>
                          </div>
                        )}

                        {/* Floating Live Badge */}
                        <div className="absolute top-3 left-3 bg-slate-900/80 backdrop-blur-md px-2.5 py-1 rounded-md text-[11px] font-mono text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5">
                          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                          <span>OPTICAL BUFFER ACTIVE</span>
                        </div>
                      </div>

                      {/* Analyse Action Button */}
                      <button
                        onClick={handleRunAnalysis}
                        disabled={scanState === 'scanning'}
                        className="w-full py-3.5 rounded-2xl bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 disabled:opacity-50 text-white font-bold text-sm shadow-md shadow-emerald-600/20 transition-all flex items-center justify-center gap-2 mb-6 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
                      >
                        {scanState === 'scanning' ? (
                          <>
                            <RotateCcw className="w-4 h-4 animate-spin" />
                            <span>Processing Optical AI Model (1.5s)...</span>
                          </>
                        ) : (
                          <>
                            <Sparkles className="w-4 h-4" />
                            <span>Analyse {selectedSampleImage}</span>
                          </>
                        )}
                      </button>

                      {/* Scan Results Panel in JetBrains Mono */}
                      {scanState === 'result' && (
                        <div className="p-5 rounded-2xl bg-slate-900 text-slate-100 border border-slate-800 font-mono text-xs animate-fade-in">
                          <div className="flex items-start justify-between border-b border-slate-800 pb-4 mb-4 gap-4 flex-wrap">
                            <div>
                              <span className="text-[11px] text-slate-400 uppercase tracking-widest block mb-1">
                                DETECTION RESULT
                              </span>
                              <div className="flex items-center gap-2 flex-wrap">
                                {scanResult.status === 'NO_OBVIOUS_VISIBLE_DEFECT' && (
                                  <span className="px-2.5 py-1 rounded-md bg-emerald-950 text-emerald-300 border border-emerald-700 font-bold">
                                    NO_OBVIOUS_VISIBLE_DEFECT
                                  </span>
                                )}
                                {scanResult.status === 'NEEDS_REVIEW' && (
                                  <span className="px-2.5 py-1 rounded-md bg-amber-950 text-amber-300 border border-amber-700 font-bold">
                                    NEEDS_REVIEW
                                  </span>
                                )}
                                {scanResult.status === 'VISIBLE_DETERIORATION' && (
                                  <span className="px-2.5 py-1 rounded-md bg-rose-950 text-rose-300 border border-rose-700 font-bold">
                                    VISIBLE_DETERIORATION
                                  </span>
                                )}
                                <span className="text-slate-400 text-[11px]">
                                  {scanResult.visibleQuality}
                                </span>
                              </div>
                            </div>

                            {/* Radial Confidence Gauge */}
                            <SemicircleGauge
                              score={scanResult.confidence}
                              status={scanResult.status}
                            />
                          </div>

                          {/* Sensor Metric Grid */}
                          <div className="grid grid-cols-2 gap-3 text-[11px] mb-5">
                            <div className="bg-slate-950/70 p-2.5 rounded-lg border border-slate-800">
                              <span className="text-slate-500 block">Vapor Core</span>
                              <span className="text-slate-200 font-medium">
                                {scanResult.metrics.steamIntegrity}
                              </span>
                            </div>
                            <div className="bg-slate-950/70 p-2.5 rounded-lg border border-slate-800">
                              <span className="text-slate-500 block">Surface Oxidation</span>
                              <span className="text-slate-200 font-medium">
                                {scanResult.metrics.surfaceOxidation}
                              </span>
                            </div>
                            <div className="bg-slate-950/70 p-2.5 rounded-lg border border-slate-800">
                              <span className="text-slate-500 block">Vessel Enclosure</span>
                              <span className="text-slate-200 font-medium">
                                {scanResult.metrics.containerSeals}
                              </span>
                            </div>
                            <div className="bg-slate-950/70 p-2.5 rounded-lg border border-slate-800">
                              <span className="text-slate-500 block">Moisture Ratio</span>
                              <span className="text-slate-200 font-medium">
                                {scanResult.metrics.moistureRetention}
                              </span>
                            </div>
                          </div>

                          {/* Non-Negotiable Warning inside Panel */}
                          <div className="p-3 rounded-lg bg-amber-950/50 border border-amber-800/80 text-amber-200 text-[11px] leading-relaxed mb-4">
                            <AlertTriangle className="w-4 h-4 text-amber-400 inline mr-1.5 -mt-0.5" />
                            <strong>Warning:</strong> FreshGuard output is supporting evidence, not a food-safety certificate. Uncertain predictions fail closed: show HOLD – needs human assessor, never Safe.
                          </div>

                          {/* Submit Action */}
                          <div className="flex items-center justify-between pt-2">
                            <button
                              onClick={() => setScanState('idle')}
                              className="text-slate-400 hover:text-white underline text-xs"
                            >
                              Reset Scanner
                            </button>
                            <button
                              onClick={handleSubmitFormalReview}
                              className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-sans font-bold text-xs transition-colors flex items-center gap-1.5"
                            >
                              <FileCheck className="w-3.5 h-3.5" />
                              <span>Submit for Formal Review</span>
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* TAB 2: QUALITY RISK SIMULATOR */}
                  {freshGuardTab === 'risk' && (
                    <div className="space-y-5 animate-fade-in">
                      <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600">
                        Simulate the dynamic risk model based on storage container, core cooking temperature, and time elapsed.
                      </div>

                      {/* Food Category Selector */}
                      <div>
                        <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                          Food Preparation Category
                        </label>
                        <select
                          value={riskCategory}
                          onChange={(e) => setRiskCategory(e.target.value)}
                          className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                        >
                          <option value="Cooked Grain">Cooked Grain (Biryani, Pulao, Steamed Rice)</option>
                          <option value="Gravy/Dairy">Lentils, Paneer & Dairy Gravies</option>
                          <option value="Bread/Roti">Baked Breads (Roti, Naan, Paratha)</option>
                          <option value="Raw Produce">Fresh Cut Produce & Salad Greens</option>
                        </select>
                      </div>

                      {/* Hours Slider */}
                      <div>
                        <div className="flex justify-between items-center text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                          <span>Hours Since Cooked</span>
                          <span className="font-mono text-slate-900 font-bold">{riskHours} Hours</span>
                        </div>
                        <input
                          type="range"
                          min="1"
                          max="12"
                          step="0.5"
                          value={riskHours}
                          onChange={(e) => setRiskHours(parseFloat(e.target.value))}
                          className="w-full accent-emerald-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
                        />
                        <div className="flex justify-between text-[11px] text-slate-400 mt-1">
                          <span>1h (Fresh)</span>
                          <span>4h (Critical Threshold)</span>
                          <span>12h (Spoiled)</span>
                        </div>
                      </div>

                      {/* Temperature Slider */}
                      <div>
                        <div className="flex justify-between items-center text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                          <span>Storage Probe Temperature</span>
                          <span className="font-mono text-slate-900 font-bold">{riskTemp}°C</span>
                        </div>
                        <input
                          type="range"
                          min="15"
                          max="80"
                          step="1"
                          value={riskTemp}
                          onChange={(e) => setRiskTemp(parseInt(e.target.value, 10))}
                          className="w-full accent-emerald-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
                        />
                        <div className="flex justify-between text-[11px] text-slate-400 mt-1">
                          <span>15°C (Ambient Danger)</span>
                          <span>60°C (Hot Holding Minimum)</span>
                          <span>80°C</span>
                        </div>
                      </div>

                      {/* Container Type */}
                      <div>
                        <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                          Container Insulation Type
                        </label>
                        <select
                          value={riskContainer}
                          onChange={(e) => setRiskContainer(e.target.value)}
                          className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                        >
                          <option value="Insulated Cambro">Insulated Stainless Cambro (Food Grade)</option>
                          <option value="Sealed Chafing Trays">Sealed Stainless Chafing Trays</option>
                          <option value="Plastic Tub">Uninsulated Plastic Tub</option>
                          <option value="Open Food Crates">Open Food Crates (High Exposure)</option>
                        </select>
                      </div>

                      {/* Calculated Dynamic Risk Bar */}
                      <div className="p-4 rounded-2xl bg-slate-100 border border-slate-200">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                            Thermal & Microbiological Risk Score:
                          </span>
                          <span className="font-mono font-bold text-sm tabular-nums">
                            {riskCalculation.score} / 100
                          </span>
                        </div>

                        {/* Progress Bar */}
                        <div className="w-full h-3 bg-slate-200 rounded-full overflow-hidden mb-3">
                          <div
                            className={`h-full ${riskCalculation.barColor} transition-all duration-300`}
                            style={{ width: `${riskCalculation.score}%` }}
                          />
                        </div>

                        <div className="flex items-center justify-between text-xs">
                          <span className="text-slate-500">Routing Decision:</span>
                          <span
                            className={`px-2.5 py-1 rounded-full font-bold border text-[11px] ${riskCalculation.colorClass}`}
                          >
                            {riskCalculation.decision}
                          </span>
                        </div>
                      </div>

                      {/* Fail-closed reminder */}
                      <div className="text-[11px] text-slate-500 leading-normal border-l-2 border-amber-500 pl-3">
                        <strong>Fail-Closed Policy:</strong> If probe temperature dips below 60°C and time exceeds 4 hours, human delivery is prohibited without direct sensory sign-off.
                      </div>
                    </div>
                  )}

                  {/* TAB 3: HISTORY */}
                  {freshGuardTab === 'history' && (
                    <div className="animate-fade-in">
                      <div className="text-xs text-slate-500 mb-3 flex items-center justify-between">
                        <span>Showing recent sample inspection logs ({batches.length})</span>
                        <span className="font-mono text-emerald-700 font-semibold">Live Prototype State</span>
                      </div>

                      <div className="overflow-x-auto border border-slate-200 rounded-2xl">
                        <table className="w-full text-left text-xs text-slate-700">
                          <thead className="bg-slate-100 text-slate-900 font-semibold border-b border-slate-200">
                            <tr>
                              <th className="py-3 px-3">Batch ID</th>
                              <th className="py-3 px-3">Kitchen</th>
                              <th className="py-3 px-3">Temp</th>
                              <th className="py-3 px-3">FreshGuard Status</th>
                              <th className="py-3 px-3">Destination</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-100">
                            {batches.map((batch) => (
                              <tr key={batch.id} className="hover:bg-slate-50 transition-colors">
                                <td className="py-2.5 px-3 font-mono font-bold text-slate-900">
                                  {batch.id}
                                </td>
                                <td className="py-2.5 px-3 font-medium truncate max-w-[120px]">
                                  {batch.kitchen}
                                </td>
                                <td className="py-2.5 px-3 font-mono">{batch.temp}</td>
                                <td className="py-2.5 px-3">
                                  {batch.status === 'NO_OBVIOUS_VISIBLE_DEFECT' && (
                                    <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 text-[10px] font-bold">
                                      PASSED
                                    </span>
                                  )}
                                  {batch.status === 'NEEDS_REVIEW' && (
                                    <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-800 text-[10px] font-bold">
                                      HOLD
                                    </span>
                                  )}
                                  {batch.status === 'VISIBLE_DETERIORATION' && (
                                    <span className="px-2 py-0.5 rounded bg-rose-100 text-rose-800 text-[10px] font-bold">
                                      DIVERT
                                    </span>
                                  )}
                                  {batch.status === 'ACCEPTED_BY_RECIPIENT' && (
                                    <span className="px-2 py-0.5 rounded bg-blue-100 text-blue-800 text-[10px] font-bold">
                                      CLAIMED
                                    </span>
                                  )}
                                </td>
                                <td className="py-2.5 px-3 truncate max-w-[130px] text-slate-500">
                                  {batch.destination}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ==========================================
            SECTION 4: ORGANIC WASTE ROUTING (REVERSED LAYOUT)
        ========================================== */}
        <section id="organic-routing" className="py-14 sm:py-20 bg-white border-y border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Demo Banner */}
            <DemoBanner className="mb-10 max-w-2xl mx-auto" />

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              {/* Left Column: Image & Circular Chart (Reversed from Section 3) */}
              <div className="lg:col-span-5 order-2 lg:order-1 flex flex-col gap-6">
                <div className="relative aspect-[4/3] rounded-3xl overflow-hidden shadow-xl border border-slate-200 bg-emerald-950">
                  <img
                    src="https://images.unsplash.com/photo-1589923188900-85dae523342b?auto=format&fit=crop&w=1000&q=80"
                    alt="Clean vegetable trimmings and peelings prepared for organic composting"
                    loading="lazy"
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.currentTarget.style.display = 'none';
                    }}
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-950/70 via-transparent to-transparent" />
                  <div className="absolute bottom-4 left-4 right-4 text-white">
                    <span className="text-[11px] font-mono uppercase tracking-wider bg-lime-500 text-slate-950 font-bold px-2 py-0.5 rounded">
                      Zero-Landfill Model
                    </span>
                    <p className="text-sm font-medium mt-1 text-slate-200">
                      100% of organic discards converted to Bio-CNG, cattle feed & fertile compost.
                    </p>
                  </div>
                </div>

                {/* Donut Chart: Where It Goes */}
                <div className="potbhar-card p-5 bg-slate-50 border border-slate-200 rounded-2xl">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-outfit font-bold text-sm text-slate-900">
                      Where Organic Surplus Goes (190 kg)
                    </h4>
                    <span className="text-[11px] font-mono text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">
                      Sample Share
                    </span>
                  </div>

                  <div className="h-44 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={ORGANIC_ROUTING_DATA}
                          cx="50%"
                          cy="50%"
                          innerRadius={45}
                          outerRadius={70}
                          paddingAngle={3}
                          dataKey="value"
                        >
                          {ORGANIC_ROUTING_DATA.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip
                          formatter={(value, name) => [`${value} kg`, name]}
                          contentStyle={{
                            backgroundColor: '#0f172a',
                            borderRadius: '12px',
                            border: 'none',
                            color: '#fff',
                            fontSize: '12px'
                          }}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>

                  {/* Donut Legend */}
                  <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-200 text-center">
                    {ORGANIC_ROUTING_DATA.map((item) => (
                      <div key={item.name} className="flex flex-col items-center">
                        <div className="flex items-center gap-1 text-[11px] font-medium text-slate-600">
                          <span
                            className="w-2 h-2 rounded-full"
                            style={{ backgroundColor: item.color }}
                          />
                          <span className="truncate">{item.name.split(' ')[0]}</span>
                        </div>
                        <span className="font-mono text-xs font-bold text-slate-900 tabular-nums">
                          {item.value} kg ({item.share})
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Right Column: Copy & 3-Step Timeline */}
              <div className="lg:col-span-7 order-1 lg:order-2 flex flex-col justify-center">
                <span className="text-xs uppercase tracking-wider font-semibold text-lime-700 bg-lime-50 border border-lime-200 px-3 py-1 rounded-full self-start">
                  Circular Bio-Economy
                </span>
                <h2 className="font-outfit text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight mt-3 mb-4">
                  Closing the Loop: From Waste to Worth
                </h2>
                <p className="text-base text-slate-600 leading-relaxed mb-6">
                  Food safety is absolute. When meals cannot be served to humans due to cold-chain lapse or excessive holding, our closed-loop routing ensures zero organic matter enters methane-generating municipal landfills.
                </p>

                {/* Two Feature Rows */}
                <div className="space-y-4 mb-8">
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex items-start gap-3.5">
                    <div className="w-10 h-10 rounded-xl bg-lime-100 text-lime-700 flex items-center justify-center shrink-0">
                      <Flame className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-slate-900">
                        Anaerobic Bio-CNG Energy & Organic Khaad
                      </h4>
                      <p className="text-xs text-slate-600 mt-0.5">
                        High-moisture cooked leftovers undergo controlled microbial biomethanation, producing clean cooking gas and chemical-free organic fertilizer for urban gardens.
                      </p>
                    </div>
                  </div>

                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex items-start gap-3.5">
                    <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center shrink-0">
                      <Award className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-slate-900">
                        Gaushala & Animal Welfare Fodder Route
                      </h4>
                      <p className="text-xs text-slate-600 mt-0.5">
                        Clean vegetarian cereal grains, dry rotis, and non-spicy vegetable trimmings are separated and routed to local certified animal shelters.
                      </p>
                    </div>
                  </div>
                </div>

                {/* 3-Step Interactive Timeline */}
                <div className="border-t border-slate-200 pt-6">
                  <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wider mb-4">
                    Continuous Diversion Lifecycle:
                  </h4>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    {[
                      {
                        step: '1. Segregate',
                        title: 'Source Separation',
                        desc: 'Kitchen bins sort edible meals from peelings.'
                      },
                      {
                        step: '2. Match',
                        title: 'Processor Matching',
                        desc: 'Nearest digester or Gaushala dispatched.'
                      },
                      {
                        step: '3. Handshake',
                        title: 'Weighbridge Receipt',
                        desc: 'Digital intake logged to carbon ledger.'
                      }
                    ].map((item, idx) => (
                      <div key={idx} className="p-3.5 rounded-xl bg-white border border-slate-200">
                        <span className="text-[11px] font-mono font-bold text-emerald-700 block">
                          {item.step}
                        </span>
                        <h5 className="font-bold text-xs text-slate-900 mt-1">{item.title}</h5>
                        <p className="text-[11px] text-slate-500 mt-0.5 leading-snug">{item.desc}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ==========================================
            SECTION 5: IMPACT ANALYTICS (RECONCILED NUMBERS)
        ========================================== */}
        <section id="impact" className="py-14 sm:py-20 bg-slate-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Header */}
            <div className="text-center max-w-3xl mx-auto mb-6">
              <span className="text-xs uppercase tracking-wider font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full">
                Verified Material Accounting
              </span>
              <h2 className="font-outfit text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight mt-3 mb-3">
                Transparent Impact Telemetry
              </h2>
              <p className="text-base text-slate-600">
                Total reported volume reconciles exactly across recovery, composting, and holding stages.
              </p>
            </div>

            {/* Persistent Amber Demo Banner */}
            <DemoBanner className="mb-8 max-w-3xl mx-auto" />

            {/* Impact Tabs */}
            <div className="flex justify-center mb-10">
              <div className="inline-flex p-1 bg-white rounded-2xl border border-slate-200 shadow-xs">
                {[
                  { id: 'overview', label: 'Overview & Funnel' },
                  { id: 'pathways', label: 'Pathway Distribution' },
                  { id: 'timeline', label: '8-Week Timeline' }
                ].map((t) => (
                  <button
                    key={t.id}
                    onClick={() => setImpactTab(t.id)}
                    className={`px-5 py-2.5 rounded-xl text-sm font-bold transition-all ${
                      impactTab === t.id
                        ? 'bg-emerald-600 text-white shadow-sm'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    {t.label}
                  </button>
                ))}
              </div>
            </div>

            {/* TAB 1: OVERVIEW */}
            {impactTab === 'overview' && (
              <div className="space-y-8 animate-fade-in">
                {/* 4 Stat Cards with Mini Sparklines */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 items-stretch">
                  {/* Card 1 */}
                  <div className="potbhar-card p-6 h-full flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between text-xs text-slate-500 font-semibold uppercase tracking-wider mb-2">
                        <span>Reported Volume</span>
                        <Utensils className="w-4 h-4 text-emerald-600" />
                      </div>
                      <div className="font-outfit text-3xl sm:text-4xl font-extrabold text-slate-900 tabular-nums">
                        1,250 <span className="text-sm font-semibold text-slate-500">kg</span>
                      </div>
                      <p className="text-xs text-slate-500 mt-1">
                        100% surplus input reconciled
                      </p>
                    </div>

                    {/* Sparkline SVG */}
                    <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                      <span className="text-xs font-mono text-emerald-700 font-bold">+18% this month</span>
                      <svg className="w-20 h-6 text-emerald-500" viewBox="0 0 80 24" fill="none">
                        <path
                          d="M0 18 Q 20 6, 40 14 T 80 4"
                          stroke="currentColor"
                          strokeWidth="2.5"
                          fill="none"
                        />
                      </svg>
                    </div>
                  </div>

                  {/* Card 2 */}
                  <div className="potbhar-card p-6 h-full flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between text-xs text-slate-500 font-semibold uppercase tracking-wider mb-2">
                        <span>Meals Provided</span>
                        <HeartHandshake className="w-4 h-4 text-emerald-600" />
                      </div>
                      <div className="font-outfit text-3xl sm:text-4xl font-extrabold text-emerald-700 tabular-nums">
                        2,375
                      </div>
                      <p className="text-xs text-slate-500 mt-1">
                        Based on standard 0.4 kg portion
                      </p>
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                      <span className="text-xs font-mono text-emerald-700 font-bold">950 kg delivered</span>
                      <svg className="w-20 h-6 text-emerald-500" viewBox="0 0 80 24" fill="none">
                        <path
                          d="M0 20 Q 25 12, 50 8 T 80 2"
                          stroke="currentColor"
                          strokeWidth="2.5"
                          fill="none"
                        />
                      </svg>
                    </div>
                  </div>

                  {/* Card 3 */}
                  <div className="potbhar-card p-6 h-full flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between text-xs text-slate-500 font-semibold uppercase tracking-wider mb-2">
                        <span>CO₂e Avoided</span>
                        <Leaf className="w-4 h-4 text-lime-600" />
                      </div>
                      <div className="font-outfit text-3xl sm:text-4xl font-extrabold text-slate-900 tabular-nums">
                        2,375 <span className="text-sm font-semibold text-slate-500">kg</span>
                      </div>
                      <p className="text-xs text-slate-500 mt-1">
                        Avoided organic methane emissions
                      </p>
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                      <span className="text-xs font-mono text-lime-700 font-bold">1.9 kg CO₂e / kg food</span>
                      <svg className="w-20 h-6 text-lime-600" viewBox="0 0 80 24" fill="none">
                        <path
                          d="M0 16 Q 20 18, 45 9 T 80 3"
                          stroke="currentColor"
                          strokeWidth="2.5"
                          fill="none"
                        />
                      </svg>
                    </div>
                  </div>

                  {/* Card 4 */}
                  <div className="potbhar-card p-6 h-full flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between text-xs text-slate-500 font-semibold uppercase tracking-wider mb-2">
                        <span>Landfill Diversion</span>
                        <Sparkles className="w-4 h-4 text-amber-500" />
                      </div>
                      <div className="font-outfit text-3xl sm:text-4xl font-extrabold text-amber-600 tabular-nums">
                        93.6%
                      </div>
                      <p className="text-xs text-slate-500 mt-1">
                        1,170 kg redirected to people or soil
                      </p>
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                      <span className="text-xs font-mono text-amber-700 font-bold">Zero toxic tipping</span>
                      <svg className="w-20 h-6 text-amber-500" viewBox="0 0 80 24" fill="none">
                        <path
                          d="M0 22 Q 25 15, 50 10 T 80 4"
                          stroke="currentColor"
                          strokeWidth="2.5"
                          fill="none"
                        />
                      </svg>
                    </div>
                  </div>
                </div>

                {/* FUNNEL & FLOW VISUALIZATION */}
                <div className="potbhar-card p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl">
                  <div className="flex items-center justify-between mb-6 flex-wrap gap-2">
                    <div>
                      <h3 className="font-outfit font-bold text-lg text-slate-900">
                        Batch Verification & Delivery Funnel
                      </h3>
                      <p className="text-xs text-slate-500 mt-0.5">
                        Traceability from donor kitchen intake to shelter doorstep intake
                      </p>
                    </div>
                    <span className="text-xs font-mono font-bold text-emerald-800 bg-emerald-100 px-3 py-1 rounded-full">
                      Reconciled Total: 1,250 kg
                    </span>
                  </div>

                  {/* Funnel Bars */}
                  <div className="space-y-4">
                    {/* Step 1: Reported */}
                    <div>
                      <div className="flex justify-between items-center text-xs font-semibold mb-1.5">
                        <span className="text-slate-800">1. Total Surplus Reported</span>
                        <span className="font-mono tabular-nums text-slate-900">
                          1,250 kg (100%)
                        </span>
                      </div>
                      <div className="w-full h-8 bg-slate-100 rounded-xl overflow-hidden p-1">
                        <div className="w-full h-full bg-slate-800 rounded-lg flex items-center px-3 text-[11px] font-mono text-white font-bold">
                          1,250 kg Logged from Commercial Kitchens
                        </div>
                      </div>
                    </div>

                    {/* Step 2: Approved */}
                    <div>
                      <div className="flex justify-between items-center text-xs font-semibold mb-1.5">
                        <span className="text-emerald-800">
                          2. Approved by FreshGuard & Assessors
                        </span>
                        <span className="font-mono tabular-nums text-emerald-700">
                          980 kg (78.4%)
                        </span>
                      </div>
                      <div className="w-full h-8 bg-slate-100 rounded-xl overflow-hidden p-1">
                        <div
                          className="h-full bg-emerald-600 rounded-lg flex items-center px-3 text-[11px] font-mono text-white font-bold transition-all duration-500"
                          style={{ width: '78.4%' }}
                        >
                          980 kg Hot & Safe
                        </div>
                      </div>
                    </div>

                    {/* Step 3: Delivered */}
                    <div>
                      <div className="flex justify-between items-center text-xs font-semibold mb-1.5">
                        <span className="text-emerald-900">
                          3. Confirmed Delivered to Community Shelters
                        </span>
                        <span className="font-mono tabular-nums text-emerald-800 font-bold">
                          950 kg (76.0%)
                        </span>
                      </div>
                      <div className="w-full h-8 bg-slate-100 rounded-xl overflow-hidden p-1">
                        <div
                          className="h-full bg-gradient-to-r from-emerald-600 to-emerald-700 rounded-lg flex items-center px-3 text-[11px] font-mono text-white font-bold transition-all duration-500"
                          style={{ width: '76.0%' }}
                        >
                          950 kg (2,375 Meals)
                        </div>
                      </div>
                    </div>

                    {/* Remaining 30kg note */}
                    <div className="text-right text-[11px] text-slate-500 font-mono">
                      *Remaining 30 kg approved surplus is currently in transit to Asha Community Kitchen.
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* TAB 2: PATHWAYS */}
            {impactTab === 'pathways' && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch animate-fade-in">
                {/* Donut Chart Reconciled to 1,250 kg */}
                <div className="lg:col-span-6 potbhar-card p-6 sm:p-8 bg-white flex flex-col justify-between">
                  <div>
                    <h3 className="font-outfit font-bold text-lg text-slate-900 mb-1">
                      Surplus Volume Reconciled: 1,250 kg
                    </h3>
                    <p className="text-xs text-slate-500 mb-4">
                      Complete accounting: 950 + 190 + 80 + 30 = 1,250 kg.
                    </p>

                    <div className="h-64 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={PATHWAY_DATA}
                            cx="50%"
                            cy="50%"
                            innerRadius={65}
                            outerRadius={95}
                            paddingAngle={3}
                            dataKey="value"
                          >
                            {PATHWAY_DATA.map((entry, index) => (
                              <Cell key={`pathway-cell-${index}`} fill={entry.color} />
                            ))}
                          </Pie>
                          <Tooltip
                            formatter={(value, name) => [`${value} kg`, name]}
                            contentStyle={{
                              backgroundColor: '#0f172a',
                              borderRadius: '12px',
                              border: 'none',
                              color: '#fff',
                              fontSize: '12px'
                            }}
                          />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Pathways Legend */}
                  <div className="grid grid-cols-2 gap-3 pt-4 border-t border-slate-100">
                    {PATHWAY_DATA.map((item) => (
                      <div key={item.name} className="flex items-start gap-2 text-xs">
                        <span
                          className="w-3 h-3 rounded-full mt-0.5 shrink-0"
                          style={{ backgroundColor: item.color }}
                        />
                        <div>
                          <span className="font-medium text-slate-800 block leading-tight">
                            {item.name}
                          </span>
                          <span className="font-mono text-slate-500 text-[11px] font-bold tabular-nums">
                            {item.value} kg ({item.share})
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Horizontal Bar Chart by Food Category */}
                <div className="lg:col-span-6 potbhar-card p-6 sm:p-8 bg-white flex flex-col justify-between">
                  <div>
                    <h3 className="font-outfit font-bold text-lg text-slate-900 mb-1">
                      Recovered Volume by Food Category
                    </h3>
                    <p className="text-xs text-slate-500 mb-6">
                      Distribution across major Indian banquet preparations (sample breakdown)
                    </p>

                    <div className="h-64 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          layout="vertical"
                          data={CATEGORY_BAR_DATA}
                          margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
                          <XAxis type="number" unit=" kg" tick={{ fontSize: 11, fill: '#64748b' }} />
                          <YAxis
                            dataKey="category"
                            type="category"
                            width={110}
                            tick={{ fontSize: 11, fill: '#334155' }}
                          />
                          <Tooltip
                            formatter={(value) => [`${value} kg`, 'Total Recovered']}
                            contentStyle={{
                              backgroundColor: '#0f172a',
                              borderRadius: '12px',
                              border: 'none',
                              color: '#fff',
                              fontSize: '12px'
                            }}
                          />
                          <Bar dataKey="kg" fill="#059669" radius={[0, 6, 6, 0]} barSize={18} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                    <span>Highest Category: Cooked Grains (38.4%)</span>
                    <span className="font-mono text-emerald-700 font-bold">1,270 kg Total Analyzed</span>
                  </div>
                </div>
              </div>
            )}

            {/* TAB 3: TIMELINE */}
            {impactTab === 'timeline' && (
              <div className="space-y-8 animate-fade-in">
                {/* 8-Week Trend Area Chart */}
                <div className="potbhar-card p-6 sm:p-8 bg-white">
                  <div className="flex items-center justify-between mb-6 flex-wrap gap-2">
                    <div>
                      <h3 className="font-outfit font-bold text-lg text-slate-900">
                        Weekly Reported vs Delivered Volume (8 Weeks)
                      </h3>
                      <p className="text-xs text-slate-500 mt-0.5">
                        Consistently tracking &gt;75% human recovery rate across sample test cycles
                      </p>
                    </div>
                    <div className="flex items-center gap-4 text-xs font-semibold">
                      <span className="flex items-center gap-1.5 text-slate-700">
                        <span className="w-3 h-3 rounded-full bg-slate-800" />
                        Reported (kg)
                      </span>
                      <span className="flex items-center gap-1.5 text-emerald-700">
                        <span className="w-3 h-3 rounded-full bg-emerald-600" />
                        Delivered to People (kg)
                      </span>
                    </div>
                  </div>

                  <div className="h-72 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart
                        data={TIMELINE_DATA}
                        margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                      >
                        <defs>
                          <linearGradient id="colorReported" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#1e293b" stopOpacity={0.15} />
                            <stop offset="95%" stopColor="#1e293b" stopOpacity={0} />
                          </linearGradient>
                          <linearGradient id="colorDelivered" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#059669" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#059669" stopOpacity={0} />
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                        <XAxis dataKey="week" tick={{ fontSize: 12, fill: '#64748b' }} />
                        <YAxis unit=" kg" tick={{ fontSize: 12, fill: '#64748b' }} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: '#0f172a',
                            borderRadius: '12px',
                            border: 'none',
                            color: '#fff',
                            fontSize: '12px'
                          }}
                        />
                        <Area
                          type="monotone"
                          dataKey="reported"
                          stroke="#1e293b"
                          strokeWidth={2}
                          fillOpacity={1}
                          fill="url(#colorReported)"
                          name="Surplus Reported"
                        />
                        <Area
                          type="monotone"
                          dataKey="delivered"
                          stroke="#059669"
                          strokeWidth={2.5}
                          fillOpacity={1}
                          fill="url(#colorDelivered)"
                          name="Delivered to People"
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Recent Batches Table with Filter Chips */}
                <div className="potbhar-card p-6 sm:p-8 bg-white">
                  <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
                    <div>
                      <h3 className="font-outfit font-bold text-lg text-slate-900">
                        Recent Batch Dispatches (Demonstration Data)
                      </h3>
                      <p className="text-xs text-slate-500 mt-0.5">
                        Interactive sample registry of all banquet pickups and routing decisions
                      </p>
                    </div>

                    {/* Filter Chips */}
                    <div className="flex items-center gap-1.5 p-1 bg-slate-100 rounded-xl border border-slate-200">
                      {[
                        { id: 'ALL', label: 'All Batches' },
                        { id: 'DELIVERED', label: 'Delivered (Human)' },
                        { id: 'ORGANIC', label: 'Organic Compost' },
                        { id: 'HOLD', label: 'In Assessment' }
                      ].map((chip) => (
                        <button
                          key={chip.id}
                          onClick={() => setTimelineFilter(chip.id)}
                          className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                            timelineFilter === chip.id
                              ? 'bg-white text-emerald-800 shadow-xs border border-slate-200 font-bold'
                              : 'text-slate-600 hover:text-slate-900'
                          }`}
                        >
                          {chip.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="overflow-x-auto border border-slate-200 rounded-2xl">
                    <table className="w-full text-left text-xs text-slate-700">
                      <thead className="bg-slate-50 text-slate-900 font-semibold border-b border-slate-200">
                        <tr>
                          <th className="py-3.5 px-4">Batch ID</th>
                          <th className="py-3.5 px-4">Donor Kitchen</th>
                          <th className="py-3.5 px-4">Food Category</th>
                          <th className="py-3.5 px-4">Weight</th>
                          <th className="py-3.5 px-4">Core Temp</th>
                          <th className="py-3.5 px-4">FreshGuard Status</th>
                          <th className="py-3.5 px-4">Destination</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {filteredTimelineBatches.map((b) => (
                          <tr key={b.id} className="hover:bg-slate-50 transition-colors">
                            <td className="py-3 px-4 font-mono font-bold text-slate-900">{b.id}</td>
                            <td className="py-3 px-4 font-medium text-slate-900">{b.kitchen}</td>
                            <td className="py-3 px-4 text-slate-600">{b.category}</td>
                            <td className="py-3 px-4 font-mono font-semibold">{b.weightKg} kg</td>
                            <td className="py-3 px-4 font-mono">{b.temp}</td>
                            <td className="py-3 px-4">
                              {b.status === 'NO_OBVIOUS_VISIBLE_DEFECT' && (
                                <span className="px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                                  APPROVED
                                </span>
                              )}
                              {b.status === 'NEEDS_REVIEW' && (
                                <span className="px-2 py-0.5 rounded-md bg-amber-100 text-amber-800 font-bold text-[10px]">
                                  HOLD · INSPECTION
                                </span>
                              )}
                              {b.status === 'VISIBLE_DETERIORATION' && (
                                <span className="px-2 py-0.5 rounded-md bg-rose-100 text-rose-800 font-bold text-[10px]">
                                  ORGANIC DIVERT
                                </span>
                              )}
                              {b.status === 'ACCEPTED_BY_RECIPIENT' && (
                                <span className="px-2 py-0.5 rounded-md bg-blue-100 text-blue-800 font-bold text-[10px]">
                                  CLAIMED BY RECIPIENT
                                </span>
                              )}
                            </td>
                            <td className="py-3 px-4 text-slate-600 font-medium">{b.destination}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}
          </div>
        </section>
      </main>

      {/* ==========================================
          SECTION 6: FOOTER (HONESTY & LEGAL MODAL)
      ========================================== */}
      <footer className="bg-slate-900 text-slate-300 pt-16 pb-12 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-10 mb-12">
            {/* Col 1: Wordmark & Hackathon notice */}
            <div className="md:col-span-5">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-2xl bg-emerald-600 flex items-center justify-center text-white">
                  <Leaf className="w-5 h-5 -rotate-12" />
                </div>
                <span className="font-outfit font-extrabold text-2xl text-white tracking-tight">
                  POTBHAR
                </span>
                <span className="text-[11px] font-mono uppercase bg-amber-500/20 text-amber-400 font-bold px-2 py-0.5 rounded border border-amber-500/40">
                  Prototype
                </span>
              </div>
              <p className="text-xs text-slate-400 font-medium mb-4">
                "Har Pet Bhare, Har Nivala Sambhale"
              </p>
              <p className="text-sm text-slate-400 leading-relaxed max-w-sm mb-6">
                An AI-assisted hackathon prototype demonstrating algorithmic food recovery, fail-closed safety triage, and closed-loop organic waste routing.
              </p>
              <p className="text-xs text-slate-500">
                Hackathon Prototype © 2026. Non-commercial open demonstrator.
              </p>
            </div>

            {/* Col 2: Navigation Links */}
            <div className="md:col-span-3">
              <h4 className="font-outfit font-bold text-white text-sm uppercase tracking-wider mb-4">
                Quick Navigation
              </h4>
              <ul className="space-y-2.5 text-sm">
                <li>
                  <a href="#hero" className="hover:text-emerald-400 transition-colors">
                    Home
                  </a>
                </li>
                <li>
                  <a href="#how-it-works" className="hover:text-emerald-400 transition-colors">
                    How It Works
                  </a>
                </li>
                <li>
                  <a href="#freshguard" className="hover:text-emerald-400 transition-colors">
                    FreshGuard AI Scanner
                  </a>
                </li>
                <li>
                  <a href="#organic-routing" className="hover:text-emerald-400 transition-colors">
                    Organic Waste Routing
                  </a>
                </li>
                <li>
                  <a href="#impact" className="hover:text-emerald-400 transition-colors">
                    Impact Analytics
                  </a>
                </li>
              </ul>
            </div>

            {/* Col 3: Legal & Honest Policies (NO DEAD # LINKS) */}
            <div className="md:col-span-4">
              <h4 className="font-outfit font-bold text-white text-sm uppercase tracking-wider mb-4">
                Policies & Protocols
              </h4>
              <ul className="space-y-2.5 text-sm mb-6">
                <li>
                  <button
                    onClick={() => setLegalModalContent('terms')}
                    className="hover:text-emerald-400 underline transition-colors text-left"
                  >
                    Terms of Demonstration Use
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setLegalModalContent('privacy')}
                    className="hover:text-emerald-400 underline transition-colors text-left"
                  >
                    Data Privacy & Synthetic Telemetry
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setLegalModalContent('safety')}
                    className="hover:text-emerald-400 underline transition-colors text-left"
                  >
                    Fail-Closed Food Safety Protocol
                  </button>
                </li>
              </ul>

              {/* Quick Actions */}
              <div className="flex gap-2">
                <button
                  onClick={() => setDonorModalOpen(true)}
                  className="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-white border border-slate-700 transition-colors"
                >
                  Report Surplus
                </button>
                <button
                  onClick={() => setRecipientModalOpen(true)}
                  className="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-white border border-slate-700 transition-colors"
                >
                  Recipient Search
                </button>
              </div>
            </div>
          </div>

          {/* Persistent Amber Banner in Footer */}
          <div className="p-4 rounded-2xl bg-amber-950/40 border border-amber-800/60 text-amber-200 text-xs leading-relaxed flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <strong className="text-amber-300 block mb-0.5 font-bold">
                Demonstration data — not live operational results.
              </strong>
              POTBHAR is an experimental hackathon concept. All organizations (e.g. Saffron Hall Caterers, Asha Community Kitchen), metrics, and sensor telemetry shown are simulated sample data. We never claim official FSSAI certifications, 100% safety guarantees, or live commercial endorsements.
            </div>
          </div>
        </div>
      </footer>

      {/* ==========================================
          MODAL 1: AUTHENTICATION / DEMO USER
      ========================================== */}
      {authModalOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="auth-modal-title"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm animate-fade-in"
        >
          <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative animate-slide-up">
            <button
              onClick={() => setAuthModalOpen(false)}
              className="absolute top-5 right-5 text-slate-400 hover:text-slate-700 p-1"
              aria-label="Close dialog"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="text-center mb-6">
              <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center mx-auto mb-3">
                <Lock className="w-6 h-6" />
              </div>
              <h3 id="auth-modal-title" className="font-outfit font-bold text-2xl text-slate-900">
                {authTab === 'login' ? 'Sign in to POTBHAR' : 'Create Demo Account'}
              </h3>
              <p className="text-xs text-slate-500 mt-1">
                Access your donor kitchen, shelter pantry, or inspection console
              </p>
            </div>

            {/* Quick Demo Login Option */}
            <div className="mb-6 p-4 rounded-2xl bg-emerald-50 border border-emerald-200">
              <span className="text-xs font-bold text-emerald-900 block mb-2">
                ⚡ Instant Hackathon Demo Login:
              </span>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => handleDemoLogin('Donor')}
                  className="py-2 px-2 text-xs font-bold rounded-xl bg-white border border-emerald-300 text-emerald-800 hover:bg-emerald-100 transition-all text-center shadow-xs"
                >
                  Donor
                </button>
                <button
                  type="button"
                  onClick={() => handleDemoLogin('Recipient')}
                  className="py-2 px-2 text-xs font-bold rounded-xl bg-white border border-emerald-300 text-emerald-800 hover:bg-emerald-100 transition-all text-center shadow-xs"
                >
                  Shelter
                </button>
                <button
                  type="button"
                  onClick={() => handleDemoLogin('Assessor')}
                  className="py-2 px-2 text-xs font-bold rounded-xl bg-white border border-emerald-300 text-emerald-800 hover:bg-emerald-100 transition-all text-center shadow-xs"
                >
                  Assessor
                </button>
              </div>
            </div>

            {/* Simulated Form */}
            <form
              onSubmit={(e) => {
                e.preventDefault();
                if (!authEmail || !authPassword) {
                  setAuthError('Please fill in both email and password.');
                  return;
                }
                handleDemoLogin('Donor');
              }}
              className="space-y-4"
            >
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Email Address
                </label>
                <input
                  type="email"
                  value={authEmail}
                  onChange={(e) => setAuthEmail(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  placeholder="name@kitchen.internal"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Password
                </label>
                <input
                  type="password"
                  value={authPassword}
                  onChange={(e) => setAuthPassword(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>

              {authError && <p className="text-xs text-rose-600 font-semibold">{authError}</p>}

              <button
                type="submit"
                className="w-full py-3 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm shadow-md transition-all"
              >
                {authTab === 'login' ? 'Sign In' : 'Register Account'}
              </button>
            </form>

            <div className="mt-4 text-center">
              <button
                onClick={() => setAuthTab(authTab === 'login' ? 'register' : 'login')}
                className="text-xs text-slate-500 hover:text-slate-800 underline"
              >
                {authTab === 'login'
                  ? 'Need a demo registration? Switch to Register'
                  : 'Already have credentials? Switch to Log in'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ==========================================
          MODAL 2: DONOR "REPORT SURPLUS FOOD" (MULTI-STEP)
      ========================================== */}
      {donorModalOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="donor-modal-title"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm animate-fade-in"
        >
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative max-h-[90vh] overflow-y-auto animate-slide-up">
            <button
              onClick={() => setDonorModalOpen(false)}
              className="absolute top-5 right-5 text-slate-400 hover:text-slate-700 p-1"
              aria-label="Close dialog"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Header */}
            <div className="mb-6">
              <div className="flex items-center gap-2 mb-1">
                <span className="w-6 h-6 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-xs font-mono">
                  {donorStep}
                </span>
                <span className="text-xs font-mono text-slate-400 uppercase tracking-widest">
                  Step {donorStep} of 3
                </span>
              </div>
              <h3 id="donor-modal-title" className="font-outfit font-bold text-2xl text-slate-900">
                Report Surplus Banquet Food
              </h3>
              <p className="text-xs text-slate-500 mt-1">
                Log freshly prepared banquet meals for instant routing
              </p>
            </div>

            <form onSubmit={handleDonorSubmit}>
              {/* Step 1: Details */}
              {donorStep === 1 && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                      Donor Organization / Kitchen Name
                    </label>
                    <input
                      type="text"
                      required
                      value={newSurplus.kitchen}
                      onChange={(e) => setNewSurplus({ ...newSurplus, kitchen: e.target.value })}
                      className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                      Dish Description
                    </label>
                    <input
                      type="text"
                      required
                      value={newSurplus.foodName}
                      onChange={(e) => setNewSurplus({ ...newSurplus, foodName: e.target.value })}
                      className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                        Surplus Weight (kg)
                      </label>
                      <input
                        type="number"
                        min="5"
                        max="500"
                        required
                        value={newSurplus.weightKg}
                        onChange={(e) =>
                          setNewSurplus({ ...newSurplus, weightKg: parseFloat(e.target.value) })
                        }
                        className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none font-mono"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                        Category
                      </label>
                      <select
                        value={newSurplus.category}
                        onChange={(e) => setNewSurplus({ ...newSurplus, category: e.target.value })}
                        className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                      >
                        <option value="Cooked Grain">Cooked Grain</option>
                        <option value="Gravy/Dairy">Lentils / Dal</option>
                        <option value="Bread/Roti">Roti / Bread</option>
                        <option value="Dessert">Sweets</option>
                      </select>
                    </div>
                  </div>

                  <div className="pt-4 flex justify-end">
                    <button
                      type="button"
                      onClick={() => setDonorStep(2)}
                      className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm transition-all flex items-center gap-1.5"
                    >
                      <span>Continue to Quality Check</span>
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              )}

              {/* Step 2: Quality & Thermal Verification */}
              {donorStep === 2 && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                      Current Surface Probe Temperature (°C)
                    </label>
                    <input
                      type="number"
                      min="20"
                      max="90"
                      required
                      value={newSurplus.temp}
                      onChange={(e) =>
                        setNewSurplus({ ...newSurplus, temp: parseFloat(e.target.value) })
                      }
                      className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-mono focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    />
                    <span className="text-[11px] text-slate-500 mt-0.5 block">
                      Target hot holding: &gt;60°C for priority human recovery
                    </span>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                      Hours Since Completed Cooking
                    </label>
                    <input
                      type="number"
                      min="0.5"
                      max="12"
                      step="0.5"
                      required
                      value={newSurplus.hoursCooked}
                      onChange={(e) =>
                        setNewSurplus({ ...newSurplus, hoursCooked: parseFloat(e.target.value) })
                      }
                      className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-mono focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                      Storage Packaging
                    </label>
                    <select
                      value={newSurplus.container}
                      onChange={(e) => setNewSurplus({ ...newSurplus, container: e.target.value })}
                      className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    >
                      <option value="Insulated Cambro">Insulated Stainless Cambro</option>
                      <option value="Sealed Chafing Trays">Sealed Stainless Chafing Trays</option>
                      <option value="Plastic Tub">Plastic Containers</option>
                    </select>
                  </div>

                  <div className="pt-4 flex justify-between">
                    <button
                      type="button"
                      onClick={() => setDonorStep(1)}
                      className="px-4 py-2.5 rounded-xl text-slate-600 hover:text-slate-900 font-semibold text-sm"
                    >
                      Back
                    </button>
                    <button
                      type="button"
                      onClick={() => setDonorStep(3)}
                      className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm transition-all flex items-center gap-1.5"
                    >
                      <span>Review & Submit</span>
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              )}

              {/* Step 3: Review & Submit */}
              {donorStep === 3 && (
                <div className="space-y-4">
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 text-xs space-y-2">
                    <div className="flex justify-between">
                      <span className="text-slate-500">Dish Name:</span>
                      <span className="font-bold text-slate-900">{newSurplus.foodName}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Declared Weight:</span>
                      <span className="font-mono font-bold text-slate-900">
                        {newSurplus.weightKg} kg (~{Math.round(newSurplus.weightKg / 0.4)} meals)
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Probe Temp:</span>
                      <span className="font-mono font-bold text-emerald-700">
                        {newSurplus.temp}°C
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Elapsed Cooking:</span>
                      <span className="font-mono text-slate-900">{newSurplus.hoursCooked} Hours</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Vessel:</span>
                      <span className="text-slate-900">{newSurplus.container}</span>
                    </div>
                  </div>

                  <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs">
                    <AlertTriangle className="w-4 h-4 text-amber-600 inline mr-1.5 -mt-0.5" />
                    <strong>Compliance Affirmation:</strong> The donor kitchen confirms food was prepared in a sanitary commercial kitchen. FreshGuard will run visual validation upon pickup van arrival.
                  </div>

                  <div className="pt-4 flex justify-between">
                    <button
                      type="button"
                      onClick={() => setDonorStep(2)}
                      className="px-4 py-2.5 rounded-xl text-slate-600 hover:text-slate-900 font-semibold text-sm"
                    >
                      Back
                    </button>
                    <button
                      type="submit"
                      className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm shadow-md transition-all flex items-center gap-1.5"
                    >
                      <CheckCircle2 className="w-4 h-4" />
                      <span>Confirm & Request Van Pickup</span>
                    </button>
                  </div>
                </div>
              )}
            </form>
          </div>
        </div>
      )}

      {/* ==========================================
          MODAL 3: RECIPIENT "FIND FOOD DONATIONS"
      ========================================== */}
      {recipientModalOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="recipient-modal-title"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm animate-fade-in"
        >
          <div className="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative max-h-[90vh] flex flex-col animate-slide-up">
            <button
              onClick={() => setRecipientModalOpen(false)}
              className="absolute top-5 right-5 text-slate-400 hover:text-slate-700 p-1"
              aria-label="Close dialog"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="mb-6">
              <h3
                id="recipient-modal-title"
                className="font-outfit font-bold text-2xl text-slate-900"
              >
                Available Food Batches (Simulated Radar)
              </h3>
              <p className="text-xs text-slate-500 mt-1">
                Verified community kitchens can claim hot surplus meals for direct serving
              </p>
            </div>

            {/* Search & Filter Bar */}
            <div className="flex flex-col sm:flex-row gap-3 mb-6">
              <div className="relative flex-1">
                <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="text"
                  value={recipientSearch}
                  onChange={(e) => setRecipientSearch(e.target.value)}
                  placeholder="Search by dish name or kitchen..."
                  className="w-full pl-9 pr-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>

              <select
                value={recipientCategoryFilter}
                onChange={(e) => setRecipientCategoryFilter(e.target.value)}
                className="px-3 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="ALL">All Categories</option>
                <option value="HUMAN">Human Verified</option>
                <option value="GRAIN">Grains & Rice</option>
                <option value="CURRY">Curries & Dals</option>
              </select>
            </div>

            {/* Batch List */}
            <div className="flex-1 overflow-y-auto space-y-3 pr-1">
              {filteredRecipientBatches.length === 0 ? (
                <div className="text-center py-12 text-slate-500 text-xs">
                  No matching surplus batches found. Try broadening your search.
                </div>
              ) : (
                filteredRecipientBatches.map((batch) => (
                  <div
                    key={batch.id}
                    className="p-4 rounded-2xl border border-slate-200 bg-slate-50/70 hover:bg-white hover:shadow-md transition-all flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
                  >
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-mono font-bold text-xs text-slate-900">
                          {batch.id}
                        </span>
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                          {batch.temp} · Hot Holding
                        </span>
                        <span className="text-slate-400 text-xs">({batch.timestamp})</span>
                      </div>
                      <h4 className="font-bold text-sm text-slate-900">{batch.category}</h4>
                      <p className="text-xs text-slate-500 mt-0.5">
                        Donor: <strong className="text-slate-700">{batch.kitchen}</strong> ·{' '}
                        {batch.weightKg} kg (~{Math.round(batch.weightKg / 0.4)} portions)
                      </p>
                    </div>

                    <button
                      onClick={() => handleAcceptBatch(batch.id)}
                      className="w-full sm:w-auto px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs transition-colors shrink-0 shadow-sm"
                    >
                      Accept Batch
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* ==========================================
          DRAWER: ROLE-BASED DASHBOARD
      ========================================== */}
      {dashboardDrawerOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="drawer-title"
          className="fixed inset-0 z-50 overflow-hidden bg-slate-950/60 backdrop-blur-sm animate-fade-in"
        >
          <div className="absolute inset-y-0 right-0 max-w-full flex pl-10">
            <div className="w-screen max-w-md bg-white shadow-2xl border-l border-slate-200 flex flex-col animate-slide-left">
              {/* Drawer Header */}
              <div className="p-6 border-b border-slate-200 flex items-center justify-between">
                <div>
                  <h3 id="drawer-title" className="font-outfit font-bold text-xl text-slate-900">
                    Role Dashboard Drawer
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Demonstration console for operational participants
                  </p>
                </div>
                <button
                  onClick={() => setDashboardDrawerOpen(false)}
                  className="p-1 text-slate-400 hover:text-slate-700"
                  aria-label="Close drawer"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Role Switcher Pills */}
              <div className="p-4 bg-slate-50 border-b border-slate-200">
                <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block mb-2">
                  Simulate Stakeholder Perspective:
                </span>
                <div className="grid grid-cols-3 gap-1.5 p-1 bg-slate-200 rounded-xl">
                  {['Donor', 'Recipient', 'Assessor'].map((role) => (
                    <button
                      key={role}
                      onClick={() => setDashboardRole(role)}
                      className={`py-1.5 text-xs font-bold rounded-lg transition-all ${
                        dashboardRole === role
                          ? 'bg-white text-emerald-800 shadow-sm'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      {role}
                    </button>
                  ))}
                </div>
              </div>

              {/* Drawer Body content by Role */}
              <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {/* ROLE 1: DONOR */}
                {dashboardRole === 'Donor' && (
                  <div className="space-y-4">
                    <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200">
                      <span className="text-xs font-bold text-emerald-800 block">
                        Saffron Hall Caterers Console
                      </span>
                      <p className="text-xs text-emerald-700 mt-1">
                        Active Donor Account · 420 kg donated this month
                      </p>
                    </div>

                    <button
                      onClick={() => {
                        setDashboardDrawerOpen(false);
                        setDonorModalOpen(true);
                      }}
                      className="w-full py-3 rounded-xl bg-emerald-600 text-white font-bold text-xs shadow-sm hover:bg-emerald-700 transition-colors"
                    >
                      + Report New Surplus Batch
                    </button>

                    <h4 className="font-outfit font-bold text-sm text-slate-900">
                      Active Pickups (Sample)
                    </h4>
                    <div className="space-y-2">
                      {batches.slice(0, 3).map((b) => (
                        <div
                          key={b.id}
                          className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs"
                        >
                          <div className="flex justify-between font-bold">
                            <span>{b.id}</span>
                            <span className="text-emerald-700">{b.weightKg} kg</span>
                          </div>
                          <p className="text-slate-600 mt-0.5">{b.category}</p>
                          <span className="text-[10px] text-slate-400 font-mono mt-1 block">
                            En route to {b.destination}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* ROLE 2: RECIPIENT */}
                {dashboardRole === 'Recipient' && (
                  <div className="space-y-4">
                    <div className="p-4 rounded-2xl bg-blue-50 border border-blue-200">
                      <span className="text-xs font-bold text-blue-800 block">
                        Asha Community Kitchen Pantry
                      </span>
                      <p className="text-xs text-blue-700 mt-1">
                        Registered Shelter · Capacity: 400 meals / day
                      </p>
                    </div>

                    <button
                      onClick={() => {
                        setDashboardDrawerOpen(false);
                        setRecipientModalOpen(true);
                      }}
                      className="w-full py-3 rounded-xl bg-blue-600 text-white font-bold text-xs shadow-sm hover:bg-blue-700 transition-colors"
                    >
                      Browse Available Surplus Radar
                    </button>

                    <h4 className="font-outfit font-bold text-sm text-slate-900">
                      Incoming Meal Allocations
                    </h4>
                    <div className="space-y-2">
                      {batches
                        .filter((b) => b.destination.includes('Asha') || b.status === 'ACCEPTED_BY_RECIPIENT')
                        .map((b) => (
                          <div
                            key={b.id}
                            className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs"
                          >
                            <div className="flex justify-between font-bold">
                              <span>{b.id}</span>
                              <span className="text-blue-700">{b.weightKg} kg</span>
                            </div>
                            <p className="text-slate-600 mt-0.5">{b.category}</p>
                            <span className="text-[10px] text-emerald-600 font-semibold mt-1 block">
                              ETA ~15 mins (Temp: {b.temp})
                            </span>
                          </div>
                        ))}
                    </div>
                  </div>
                )}

                {/* ROLE 3: ASSESSOR */}
                {dashboardRole === 'Assessor' && (
                  <div className="space-y-4">
                    <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200">
                      <span className="text-xs font-bold text-amber-900 block">
                        City Quality Assessor Unit
                      </span>
                      <p className="text-xs text-amber-800 mt-1">
                        Triage queue for borderline sensor readings
                      </p>
                    </div>

                    <h4 className="font-outfit font-bold text-sm text-slate-900">
                      Flagged Inspection Queue
                    </h4>
                    <div className="space-y-3">
                      {batches.map((b) => (
                        <div
                          key={b.id}
                          className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 text-xs"
                        >
                          <div className="flex justify-between font-bold text-slate-900 mb-1">
                            <span>{b.id}</span>
                            <span className="font-mono">{b.temp}</span>
                          </div>
                          <p className="text-slate-600 font-medium mb-1">{b.category}</p>
                          <span className="text-[10px] text-slate-500 font-mono block mb-2">
                            FreshGuard: {b.status}
                          </span>

                          <div className="flex gap-2">
                            <button
                              onClick={() => handleAssessorDecision(b.id, true)}
                              className="flex-1 py-1.5 rounded-lg bg-emerald-600 text-white font-bold text-[11px] hover:bg-emerald-700"
                            >
                              Approve
                            </button>
                            <button
                              onClick={() => handleAssessorDecision(b.id, false)}
                              className="flex-1 py-1.5 rounded-lg bg-amber-600 text-white font-bold text-[11px] hover:bg-amber-700"
                            >
                              Divert Bio
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ==========================================
          MODAL 4: LEGAL / PROTOTYPE TERMS (NO DEAD #)
      ========================================== */}
      {legalModalContent && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="legal-modal-title"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm animate-fade-in"
        >
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative animate-slide-up max-h-[85vh] overflow-y-auto">
            <button
              onClick={() => setLegalModalContent(null)}
              className="absolute top-5 right-5 text-slate-400 hover:text-slate-700 p-1"
              aria-label="Close dialog"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="mb-4">
              <span className="text-xs uppercase tracking-wider font-mono font-bold text-amber-700 bg-amber-100 px-2.5 py-0.5 rounded">
                Prototype Governance
              </span>
              <h3 id="legal-modal-title" className="font-outfit font-bold text-2xl text-slate-900 mt-2">
                {legalModalContent === 'terms' && 'Terms of Demonstration Use'}
                {legalModalContent === 'privacy' && 'Data Privacy & Synthetic Telemetry'}
                {legalModalContent === 'safety' && 'Fail-Closed Food Safety Protocol'}
              </h3>
            </div>

            <div className="text-xs text-slate-600 space-y-3 leading-relaxed border-t border-slate-100 pt-4">
              {legalModalContent === 'terms' && (
                <>
                  <p>
                    1. <strong>Hackathon Demonstrator:</strong> POTBHAR is a conceptual prototype developed exclusively for demonstration purposes. It does not provide commercial logistics, commercial catering dispatch, or formal statutory warranties.
                  </p>
                  <p>
                    2. <strong>Fictional Entities:</strong> All named organizations including "Saffron Hall Caterers", "Asha Community Kitchen", and "GreenGrove Organics" are fictitious placeholder entities.
                  </p>
                  <p>
                    3. <strong>Regulatory Disclaimers:</strong> POTBHAR is not affiliated with, endorsed by, or certified by FSSAI or any food safety authority.
                  </p>
                </>
              )}

              {legalModalContent === 'privacy' && (
                <>
                  <p>
                    1. <strong>Synthetic Telemetry:</strong> All GPS positions, infrared probe temperatures, and optical confidence outputs are algorithmically generated demonstration records.
                  </p>
                  <p>
                    2. <strong>Client-Side Processing:</strong> Images dropped or tested in the FreshGuard scanner are evaluated locally inside the demonstration environment.
                  </p>
                  <p>
                    3. <strong>No Personal Tracking:</strong> No personal browsing tracking or real phone records are harvested.
                  </p>
                </>
              )}

              {legalModalContent === 'safety' && (
                <>
                  <p>
                    1. <strong>Fail-Closed Guarantee:</strong> When sensor data is incomplete or temperature readings decline below safe hot-holding bands (&lt;60°C), the system defaults strictly to quarantine.
                  </p>
                  <p>
                    2. <strong>Human Assessor Supremacy:</strong> Automated AI signals constitute supporting evidence only. Final certification always requires certified human judgment.
                  </p>
                  <p>
                    3. <strong>Zero-Landfill Commitment:</strong> Non-recoverable batches are automatically routed to organic vermicompost and Bio-CNG digestion.
                  </p>
                </>
              )}
            </div>

            <div className="mt-6 pt-4 border-t border-slate-100 flex justify-end">
              <button
                onClick={() => setLegalModalContent(null)}
                className="px-5 py-2.5 rounded-xl bg-slate-900 text-white font-bold text-xs"
              >
                Close Policy
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
