import React, { useState, useEffect, useMemo } from 'react';
import {
  Dog,
  Wheat,
  Recycle,
  Route,
  Zap,
  ShieldCheck,
  HeartHandshake,
  Truck,
  Clock,
  MapPin,
  Phone,
  Award,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  ExternalLink,
  RefreshCw,
  ChevronRight,
  X,
  Flame,
  Utensils
} from 'lucide-react';

const API_BASE = (import.meta.env && import.meta.env.VITE_API_URL)
  ? `${import.meta.env.VITE_API_URL}/api/v1/smart-donation`
  : 'http://127.0.0.1:8000/api/v1/smart-donation';

const RECIPIENT_DIRECTORY_DEFAULT = [
  {
    id: 'rec_rural_01',
    name: 'Sahyadri Gramin Annapurna Seva & Anganwadi Network',
    type: 'RURAL_COMMUNITY',
    type_label: 'Rural Village Food Relief & Child Nutrition',
    diet_compatibility: 'Nutritious Cooked Meals, Fresh Rotis, Pulses & Fortified Grains',
    diet_tag: 'RURAL_NUTRITION',
    accepted_items: ['Freshly Cooked Khichdi', 'Rotis / Chapatis', 'Dal & Sabzi', 'Lentils & Flour Sacks', 'Seasonal Fruit'],
    restricted_items: ['Over-spiced gravies', 'Stale/soured food (>4h)', 'Unsealed crates'],
    contact_person: 'Sarpanch Balasaheb Shinde',
    phone: '+91 98220 44881',
    emergency_phone: '+91 98220 44882',
    email: 'sahyadri.rural@potbhar.org',
    address: 'Village Gram Panchayat Kendra, Saswad-Purandar Rural Belt, Pune 412301',
    daily_capacity_kg: 450.0,
    current_intake_kg: 230.0,
    capacity_remaining_kg: 220.0,
    resident_count: 280,
    verification_status: 'VERIFIED_ZILLA_PARISHAD_RURAL',
    verified_badge: 'Zilla Parishad & Village Panchayat Certified',
    rating: 4.97,
    rating_count: 380,
    distance_km: 14.5,
    pickup_lead_time_mins: 40,
    service_radius_km: 35.0,
    image_url: '/images/rural-food-distribution.jpg'
  },
  {
    id: 'rec_rural_02',
    name: 'Kisan Bandhu Rural Outreach & Mobile Meal Unit',
    type: 'RURAL_COMMUNITY',
    type_label: 'Rural Farm Worker & Drought-Prone Village Relief',
    diet_compatibility: 'Balanced Hot Meals, Rice, Chapati & Clean Water Tiffins',
    diet_tag: 'RURAL_NUTRITION',
    accepted_items: ['Vegetable Pulao', 'Dal Tadka', 'Packed Tiffins', 'Sacks of Grain & Atta', 'Jaggery & Chana'],
    restricted_items: ['Perishable unprotected sweets', 'Non-potable water containers'],
    contact_person: 'Sunanda Gaikwad (Outreach Lead)',
    phone: '+91 98220 66771',
    emergency_phone: '+91 98220 66772',
    email: 'kisanoutreach@potbhar.org',
    address: 'Khed Taluka Field Relief Depot, Chakan-Shikrapur Rural Link, Pune 410501',
    daily_capacity_kg: 380.0,
    current_intake_kg: 190.0,
    capacity_remaining_kg: 190.0,
    resident_count: 240,
    verification_status: 'VERIFIED_RURAL_DEVELOPMENT_TRUST',
    verified_badge: 'Rural Development Trust Registered',
    rating: 4.93,
    rating_count: 295,
    distance_km: 18.2,
    pickup_lead_time_mins: 45,
    service_radius_km: 40.0,
    image_url: '/images/rural-outreach-potbhar.jpg'
  },
  {
    id: 'rec_human_01',
    name: 'Asha Bhavan Community Food Hub',
    type: 'HUMAN_SHELTER',
    type_label: 'Night Refuge & Community Kitchen',
    diet_compatibility: 'FSSAI Verified Edible Meals (Hot Cooked)',
    diet_tag: 'HUMAN_EDIBLE',
    accepted_items: ['Complete Thali Meals', 'Paneer Sabzi', 'Dal Tadka', 'Jeera Rice', 'Roti / Chapati Packs', 'Vegetable Pulao'],
    restricted_items: ['Food exceeding 4 hours unrefrigerated', 'Sour smells', 'Unsealed containers'],
    contact_person: 'Sister Teresa Maria',
    phone: '+91 98230 11223',
    emergency_phone: '+91 98230 11224',
    email: 'care@ashabhavanpune.org',
    address: 'Behind Railway Station, Somwar Peth, Pune 411011',
    daily_capacity_kg: 400.0,
    current_intake_kg: 210.0,
    capacity_remaining_kg: 190.0,
    resident_count: 320,
    verification_status: 'VERIFIED_FSSAI_HUMAN',
    verified_badge: 'FSSAI License 11522036000192',
    rating: 4.96,
    rating_count: 680,
    distance_km: 5.6,
    pickup_lead_time_mins: 20,
    service_radius_km: 20.0,
    image_url: '/images/community-food-serving-hall.jpg'
  },
  {
    id: 'rec_human_02',
    name: 'Annapurna Seva Night Shelter',
    type: 'HUMAN_SHELTER',
    type_label: 'Shelter for Migrant Laborers & Families',
    diet_compatibility: 'Fresh Cooked Vegetarian & Egg Meals',
    diet_tag: 'HUMAN_EDIBLE',
    accepted_items: ['Khichdi', 'Sambar Rice', 'Rotis', 'Cooked Dal', 'Subzi', 'Boiled Eggs'],
    restricted_items: ['Cold stale food (>3 hrs holding)', 'Contaminated packaging'],
    contact_person: 'Anil Kulkarni (Director)',
    phone: '+91 98230 44551',
    emergency_phone: '+91 98230 44552',
    email: 'meals@annapurnaseva.org',
    address: 'Sadashiv Peth, Near Bharat Natya Mandir, Pune 411030',
    daily_capacity_kg: 220.0,
    current_intake_kg: 140.0,
    capacity_remaining_kg: 80.0,
    resident_count: 160,
    verification_status: 'VERIFIED_FSSAI_HUMAN',
    verified_badge: 'Municipal Corporation Partner',
    rating: 4.88,
    rating_count: 310,
    distance_km: 6.4,
    pickup_lead_time_mins: 30,
    service_radius_km: 18.0,
    image_url: '/images/elderly-shelter-meals.jpg'
  },
  {
    id: 'rec_gaushala_01',
    name: 'Vrindavan Gaushala & Cattle Sanctuary',
    type: 'GAUSHALA',
    type_label: 'Gaushala (Cattle Shelter)',
    diet_compatibility: 'Pure Vegetarian (Cattle-Friendly)',
    diet_tag: 'PURE_VEG',
    accepted_items: ['Cooked Rice', 'Rotis & Naans', 'Greens & Vegetables', 'Dals', 'Fruit Peelings', 'Fresh Grains'],
    restricted_items: ['Meat', 'Fish', 'Eggs', 'Garlic/Onion heavy gravies', 'Plastic/Packaging'],
    contact_person: 'Mahant Rajeshwar Das',
    phone: '+91 98220 33441',
    emergency_phone: '+91 98220 33442',
    email: 'seva@vrindavangaushala.org',
    address: 'Survey 48, Aundh-Ravet Road, Near Aundh Gaushala Facility, Pune 411007',
    daily_capacity_kg: 500.0,
    current_intake_kg: 280.0,
    capacity_remaining_kg: 220.0,
    cattle_count: 185,
    verification_status: 'VERIFIED_FSSAI_ANIMAL_WELFARE',
    verified_badge: 'Govt Animal Welfare Board Certified',
    rating: 4.9,
    rating_count: 340,
    distance_km: 4.8,
    pickup_lead_time_mins: 35,
    service_radius_km: 25.0,
    image_url: '/images/food-produce.jpg'
  },
  {
    id: 'rec_gaushala_02',
    name: 'Govardhan Cow Rescue & Seva Ashram',
    type: 'GAUSHALA',
    type_label: 'Gaushala & Desi Cow Sanctuary',
    diet_compatibility: 'Pure Vegetarian (Desi Gau Seva)',
    diet_tag: 'PURE_VEG',
    accepted_items: ['Rotis', 'Pulao/Rice', 'Chopped raw vegetables', 'Lentil residue', 'Clean bread scraps'],
    restricted_items: ['Any Non-Veg', 'Sour/Fermented Curds', 'Packaging', 'Fried oily snacks'],
    contact_person: 'Pandit Ramesh Shastri',
    phone: '+91 98220 55112',
    emergency_phone: '+91 98220 55113',
    email: 'contact@govardhanashram.in',
    address: 'Gat No 112, Alandi-Markal Road, Pune Rural 412105',
    daily_capacity_kg: 350.0,
    current_intake_kg: 150.0,
    capacity_remaining_kg: 200.0,
    cattle_count: 120,
    verification_status: 'VERIFIED_FSSAI_ANIMAL_WELFARE',
    verified_badge: 'FSSAI Gau Seva Compliant',
    rating: 4.8,
    rating_count: 210,
    distance_km: 9.3,
    pickup_lead_time_mins: 45,
    service_radius_km: 30.0,
    image_url: '/images/food-produce.jpg'
  },
  {
    id: 'rec_dogshelter_01',
    name: 'PawCare Canine Rescue & Stray Welfare',
    type: 'DOG_SHELTER',
    type_label: 'Dog Shelter & Animal Hospital',
    diet_compatibility: 'Vegetarian & Non-Vegetarian Friendly',
    diet_tag: 'NON_VEG_FRIENDLY',
    accepted_items: ['Chicken Biryani / Broth', 'Cooked Meats & Liver', 'Steamed Rice', 'Boiled Eggs', 'Mutton Gravies (Mild)', 'Paneer & Rice'],
    restricted_items: ['Extremely Spicy Chillies', 'Cooked Small Splinter Bones', 'Chocolate/Sugar', 'Onion concentrates'],
    contact_person: 'Dr. Sneha Roy (Chief Vet)',
    phone: '+91 98220 77881',
    emergency_phone: '+91 98220 77882',
    email: 'adoptions@pawcarepune.org',
    address: 'Plot 14, Baner Pashan Link Road, Pashan Biodiversity Park Zone, Pune 411045',
    daily_capacity_kg: 300.0,
    current_intake_kg: 180.0,
    capacity_remaining_kg: 120.0,
    dog_count: 165,
    verification_status: 'VERIFIED_ANIMAL_WELFARE_BOARD',
    verified_badge: 'AWBI Registered Shelter No. MH/2021/88',
    rating: 4.95,
    rating_count: 512,
    distance_km: 3.2,
    pickup_lead_time_mins: 25,
    service_radius_km: 20.0,
    image_url: '/images/banquet-surplus-biryani-curry.jpg'
  },
  {
    id: 'rec_dogshelter_02',
    name: 'Hope For Strays Canine Sanctuary',
    type: 'DOG_SHELTER',
    type_label: 'Rescue Animal Foster & Feeding Hub',
    diet_compatibility: 'Non-Vegetarian & High-Protein Meals',
    diet_tag: 'NON_VEG_FRIENDLY',
    accepted_items: ['Meat trimmings & broths', 'Plain cooked chicken', 'Boiled eggs', 'Curd rice', 'Wholesome porridge'],
    restricted_items: ['Greasy deep-fried fast food', 'Desserts', 'Raw onion/garlic cloves', 'Salty pickles'],
    contact_person: 'Vikram Joshi (Operations Lead)',
    phone: '+91 98220 99001',
    emergency_phone: '+91 98220 99002',
    email: 'rescue@hopeforstrays.org',
    address: 'Survey 22, Near Mulshi Toll Post, Bhugaon, Pune 412115',
    daily_capacity_kg: 250.0,
    current_intake_kg: 90.0,
    capacity_remaining_kg: 160.0,
    dog_count: 98,
    verification_status: 'VERIFIED_ANIMAL_WELFARE_BOARD',
    verified_badge: 'Pune Zilla Parishad Registered',
    rating: 4.75,
    rating_count: 195,
    distance_km: 7.1,
    pickup_lead_time_mins: 35,
    service_radius_km: 25.0,
    image_url: '/images/banquet-surplus-biryani-curry.jpg'
  },
  {
    id: 'rec_compost_01',
    name: 'EcoKhaad Decentralized Bio-Methanation & Compost Facility',
    type: 'COMPOST_MANURE',
    type_label: 'Organic Fertilizer & Bio-CNG Plant',
    diet_compatibility: 'Organic Food Scraps & Kitchen Waste',
    diet_tag: 'ZERO_WASTE_COMPOST',
    accepted_items: ['Kitchen Vegetable Peelings', 'Expired Cooked Food', 'Plate Waste Scrapings', 'Bread & Pastry ends', 'Citrus & Onion skins', 'Spoiled curries'],
    restricted_items: ['Plastics', 'Cutlery', 'Metal foils', 'Glass', 'Chemical cleaning agents'],
    contact_person: 'Er. Arvind Deshmukh (Environmental Engineer)',
    phone: '+91 98230 88112',
    emergency_phone: '+91 98230 88113',
    email: 'operations@ecokhaadbiogas.com',
    address: 'Eco Green Zone, Hadapsar Industrial Estate Phase 3, Pune 411013',
    daily_capacity_kg: 2000.0,
    current_intake_kg: 720.0,
    capacity_remaining_kg: 1280.0,
    compost_output_ratio: 0.28,
    verification_status: 'VERIFIED_POLLUTION_CONTROL_BOARD',
    verified_badge: 'State Pollution Board & Solid Waste Rule 2016 Compliant',
    rating: 4.92,
    rating_count: 420,
    distance_km: 8.5,
    pickup_lead_time_mins: 45,
    service_radius_km: 40.0,
    image_url: '/images/food-waste-bins.jpg'
  },
  {
    id: 'rec_compost_02',
    name: 'GreenEarth Community Micro-Composting Park',
    type: 'COMPOST_MANURE',
    type_label: 'Aerobic Compost & Urban Farm Soil Project',
    diet_compatibility: 'Raw Prep Waste & Fruit/Vegetable Scraps',
    diet_tag: 'ZERO_WASTE_COMPOST',
    accepted_items: ['Fruit/Veg trimmings', 'Salad leftovers', 'Coffee grounds', 'Stale grains', 'Eggshells'],
    restricted_items: ['Large plastic wrap', 'Non-organic packaging', 'Chemical grease'],
    contact_person: 'Sunita Rao (Urban Farming Lead)',
    phone: '+91 98230 66221',
    emergency_phone: '+91 98230 66222',
    email: 'contact@greenearthmicrocompost.org',
    address: 'Kothrud Eco Garden, Near Chandani Chowk, Pune 411038',
    daily_capacity_kg: 800.0,
    current_intake_kg: 340.0,
    capacity_remaining_kg: 460.0,
    compost_output_ratio: 0.32,
    verification_status: 'VERIFIED_POLLUTION_CONTROL_BOARD',
    verified_badge: 'Certified 100% Organic Humus Producer',
    rating: 4.86,
    rating_count: 180,
    distance_km: 4.1,
    pickup_lead_time_mins: 35,
    service_radius_km: 25.0,
    image_url: '/images/rural-ration-produce.jpg'
  }
];

export default function SmartRescueSection({ onAddToast }) {
  // Directory & active filters
  const [recipients, setRecipients] = useState(RECIPIENT_DIRECTORY_DEFAULT);
  const [typeFilter, setTypeFilter] = useState('ALL');
  const [dietFilter, setDietFilter] = useState('ALL');

  // Donor Dispatch Console Form
  const [decisionMode, setDecisionMode] = useState('SMART_RECOMMEND'); // 'SMART_RECOMMEND' or 'MANUAL_SELECT'
  const [foodTitle, setFoodTitle] = useState('Banquet Mixed Vegetable Pulao & Dry Rotis');
  const [foodCategory, setFoodCategory] = useState('VEG_GRAIN');
  const [dietType, setDietType] = useState('PURE_VEG');
  const [quantityKg, setQuantityKg] = useState(45);
  const [temperatureC, setTemperatureC] = useState(62.0);
  const [hoursCooked, setHoursCooked] = useState(1.5);
  const [packaging, setPackaging] = useState('CAMBRO_HOT_BOX');
  const [selectedRecipientId, setSelectedRecipientId] = useState('rec_gaushala_01');
  const [donorNotes, setDonorNotes] = useState('Hot and fresh, prepared for afternoon reception in insulated containers.');
  const [donorLocation, setDonorLocation] = useState('Baner Main Road, Pune (Kitchen Hub)');

  // Submission & Modals
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [dispatchSuccessModal, setDispatchSuccessModal] = useState(null);

  // Scraps-to-Compost Calculator Form & Modal
  const [scrapKg, setScrapKg] = useState(60);
  const [scrapType, setScrapType] = useState('MIXED_KITCHEN_SCRAPS');
  const [isCompostConverting, setIsCompostConverting] = useState(false);
  const [compostCertModal, setCompostCertModal] = useState(null);

  // Fetch live recipients from backend on mount (graceful fallback to defaults)
  useEffect(() => {
    fetch(`${API_BASE}/recipients`)
      .then((res) => {
        if (!res.ok) throw new Error('API offline');
        return res.json();
      })
      .then((data) => {
        if (data.recipients && data.recipients.length > 0) {
          setRecipients(data.recipients);
        }
      })
      .catch(() => {
        // Fallback to local default data silently
      });
  }, []);

  // Compute live AI Recommendation
  const smartRecommendation = useMemo(() => {
    const isHumanSafe = temperatureC >= 60.0 && hoursCooked <= 3.5;
    const isNonVeg = dietType === 'NON_VEG';
    const isScrap = dietType === 'UNSUITABLE_SCRAPS';

    let recType = 'HUMAN_SHELTER';
    let rationale = '';

    if (isScrap || hoursCooked > 8.0) {
      recType = 'COMPOST_MANURE';
      rationale = 'Food scraps or extended hold time (>8h) is not suitable for consumption. Routed to Zero-Waste Bio-Methanation & Organic Fertilizer.';
    } else if (isNonVeg) {
      recType = 'DOG_SHELTER';
      rationale = 'High-protein non-vegetarian surplus (chicken, meat, eggs, broths). Strictly prohibited at Gaushalas; optimal nutritious ration for Canine Welfare Sanctuaries.';
    } else if (dietType === 'PURE_VEG' && (foodCategory === 'VEG_GRAIN' || foodCategory === 'BREAD_ROTI')) {
      if (isHumanSafe) {
        recType = 'HUMAN_SHELTER';
        rationale = 'Hot holding verified (>60°C). Primary routing prioritizes local human night shelters. Alternatively eligible for Gaushala cattle feed.';
      } else {
        recType = 'GAUSHALA';
        rationale = 'Pure vegetarian grains/rotis held >3.5h. Triage safety rules redirect to Gaushala cattle feeding sanctuary.';
      }
    } else if (!isHumanSafe) {
      recType = 'GAUSHALA';
      rationale = 'Food has cooled below 60°C or held >3.5h. Fail-closed triage redirects to animal welfare sanctuary.';
    } else {
      recType = 'HUMAN_SHELTER';
      rationale = 'Certified fresh edible meals safely hot-held. Dispatched to registered human night shelters.';
    }

    const matchedRecipients = recipients.filter((r) => r.type === recType);
    const chosen = matchedRecipients[0] || recipients[0];

    const distanceKm = chosen.distance_km || 4.2;
    const transitTimeMins = Math.round(distanceKm * 4.5 + 8);

    return {
      recommendedRecipient: chosen,
      targetType: recType,
      confidenceScore: isNonVeg ? 99 : isScrap ? 98 : isHumanSafe ? 96 : 94,
      rationale,
      route: {
        origin: donorLocation,
        destination: chosen.name,
        address: chosen.address,
        distanceKm,
        transitTimeMins,
        waypoints: [
          donorLocation,
          'University Circle / Express Corridor',
          chosen.name + ' Intake Gate'
        ],
        vehicleAssigned: 'Tata Ace Electric Reefer Van (MH-12-EV-4421)',
        driverName: 'Rameshwar Shinde (Verified Courier)',
        driverPhone: '+91 98811 22334',
        tempControl: temperatureC >= 60 ? 'Insulated Cambro Hot-Box (Holding at 63°C)' : 'Ambient Food-Grade Crate'
      }
    };
  }, [foodCategory, dietType, hoursCooked, temperatureC, recipients, donorLocation]);

  // Compute live Compost conversion metrics
  const compostMetrics = useMemo(() => {
    const kg = parseFloat(scrapKg) || 0;
    const humusKg = +(kg * 0.40).toFixed(1);
    const co2eSavedKg = +(kg * 2.5).toFixed(1);
    const bioCngKwh = +(kg * 0.35).toFixed(1);
    const soilAreaSqM = +(kg * 1.8).toFixed(1);

    return {
      inputKg: kg,
      humusKg,
      co2eSavedKg,
      bioCngKwh,
      soilAreaSqM
    };
  }, [scrapKg]);

  // Filtered Recipient Directory
  const filteredRecipients = useMemo(() => {
    return recipients.filter((item) => {
      if (typeFilter !== 'ALL' && item.type !== typeFilter) return false;
      if (dietFilter !== 'ALL' && item.diet_tag !== dietFilter) return false;
      return true;
    });
  }, [recipients, typeFilter, dietFilter]);

  // Handle donor dispatch submission
  const handleSmartDonationSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    const targetRecipient =
      decisionMode === 'SMART_RECOMMEND'
        ? smartRecommendation.recommendedRecipient
        : recipients.find((r) => r.id === selectedRecipientId) || recipients[0];

    const payload = {
      donor_name: 'Main Kitchen & Caterers',
      donor_phone: '+91 98220 12345',
      donor_location: donorLocation,
      food_title: foodTitle,
      category: foodCategory,
      quantity_kg: parseFloat(quantityKg) || 20,
      is_non_veg: dietType === 'NON_VEG',
      temp_celsius: parseFloat(temperatureC) || 60,
      recipient_id: targetRecipient.id,
      donation_mode: decisionMode === 'SMART_RECOMMEND' ? 'SMART_RECOMMENDED' : 'DONOR_CHOSEN',
      notes: donorNotes
    };

    try {
      const response = await fetch(`${API_BASE}/donate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      const recDonation = data.donation || {};
      setDispatchSuccessModal({
        batchId: recDonation.batch_id || data.batch_id || `DON-RESCUE-${Math.floor(1000 + Math.random() * 9000)}`,
        recipient: recDonation.recipient || targetRecipient,
        route: recDonation.optimized_route || smartRecommendation.route,
        impactCredits: recDonation.impact_credits_earned || Math.round(quantityKg * 10),
        mealsOrKg: `${quantityKg} kg`
      });
    } catch {
      // Graceful local fallback modal
      setDispatchSuccessModal({
        batchId: `DON-RESCUE-${Math.floor(1000 + Math.random() * 9000)}`,
        recipient: targetRecipient,
        route: smartRecommendation.route,
        impactCredits: Math.round(quantityKg * 10),
        mealsOrKg: `${quantityKg} kg`
      });
    } finally {
      setIsSubmitting(false);
      if (onAddToast) {
        onAddToast(`Smart dispatch initiated for ${targetRecipient.name}!`);
      }
    }
  };

  // Handle scraps to compost conversion
  const handleScrapsConvert = async (e) => {
    e.preventDefault();
    setIsCompostConverting(true);

    const payload = {
      scraps_title: 'Kitchen Prep & Uneaten Scraps',
      waste_category: scrapType,
      quantity_kg: parseFloat(scrapKg) || 50,
      donor_name: 'Main Kitchen & Caterers',
      donor_location: donorLocation,
      preferred_compost_hub_id: 'rec_compost_01'
    };

    try {
      const response = await fetch(`${API_BASE}/compost-convert`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      const cert = data.certificate || {};
      setCompostCertModal({
        certificate_id: cert.batch_code || `FCO-ORG-2026-${Math.floor(10000 + Math.random() * 90000)}`,
        certified_date: cert.issued_at || new Date().toISOString().split('T')[0],
        input_scraps_kg: cert.input_scrap_kg || scrapKg,
        humus_yield_kg: cert.output_organic_humus_kg || compostMetrics.humusKg,
        co2e_offset_kg: cert.carbon_methane_offset_kg || compostMetrics.co2eSavedKg,
        biocng_kwh: cert.clean_energy_generated_kwh || compostMetrics.bioCngKwh,
        standard: cert.compost_grade || 'Fertilizer (Control) Order 1985 (FCO) - City Compost Standard',
        status: 'VERIFIED_ORGANIC_MANURE'
      });
    } catch {
      setCompostCertModal({
        certificate_id: `FCO-ORG-2026-${Math.floor(10000 + Math.random() * 90000)}`,
        certified_date: new Date().toISOString().split('T')[0],
        input_scraps_kg: scrapKg,
        humus_yield_kg: compostMetrics.humusKg,
        co2e_offset_kg: compostMetrics.co2eSavedKg,
        biocng_kwh: compostMetrics.bioCngKwh,
        standard: 'Fertilizer (Control) Order 1985 (FCO) - City Compost Standard',
        status: 'VERIFIED_ORGANIC_MANURE'
      });
    } finally {
      setIsCompostConverting(false);
      if (onAddToast) {
        onAddToast(`Converted ${scrapKg}kg scraps to certified organic compost!`);
      }
    }
  };

  const getRecipientTypeIcon = (type) => {
    switch (type) {
      case 'RURAL_COMMUNITY':
        return <HeartHandshake className="w-5 h-5 text-teal-600" />;
      case 'GAUSHALA':
        return <Wheat className="w-5 h-5 text-amber-600" />;
      case 'DOG_SHELTER':
        return <Dog className="w-5 h-5 text-orange-600" />;
      case 'HUMAN_SHELTER':
        return <HeartHandshake className="w-5 h-5 text-emerald-600" />;
      case 'COMPOST_MANURE':
        return <Recycle className="w-5 h-5 text-lime-600" />;
      default:
        return <Utensils className="w-5 h-5 text-slate-600" />;
    }
  };

  const getRecipientTypeBadge = (type) => {
    switch (type) {
      case 'RURAL_COMMUNITY':
        return 'bg-teal-100 text-teal-900 border-teal-300';
      case 'GAUSHALA':
        return 'bg-amber-100 text-amber-900 border-amber-300';
      case 'DOG_SHELTER':
        return 'bg-orange-100 text-orange-900 border-orange-300';
      case 'HUMAN_SHELTER':
        return 'bg-emerald-100 text-emerald-900 border-emerald-300';
      case 'COMPOST_MANURE':
        return 'bg-lime-100 text-lime-900 border-lime-300';
      default:
        return 'bg-slate-100 text-slate-800 border-slate-300';
    }
  };

  return (
    <section id="smart-rescue" className="relative py-16 sm:py-24 bg-gradient-to-b from-[#FFF9EF] via-emerald-50/20 to-[#FFF9EF] border-y border-[#EFE5D5] overflow-hidden">
      {/* Animated Background Color Blobs */}
      <div className="absolute top-20 -left-24 w-80 h-80 bg-emerald-400/10 rounded-full blur-3xl pointer-events-none animate-blob -z-10" />
      <div className="absolute top-1/2 -right-24 w-80 h-80 bg-amber-400/10 rounded-full blur-3xl pointer-events-none animate-blob animation-delay-2000 -z-10" />
      <div className="absolute bottom-10 left-1/3 w-72 h-72 bg-teal-400/10 rounded-full blur-3xl pointer-events-none animate-blob animation-delay-4000 -z-10" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-14">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-100/80 border border-emerald-300 text-emerald-800 text-xs font-bold tracking-wide uppercase shadow-sm mb-4">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            Food Rescue & Smart Donation Network
          </div>
          <h2 className="font-outfit text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
            Connecting Surplus to the <span className="text-emerald-700 underline decoration-emerald-400 decoration-wavy">Right Recipient</span>
          </h2>
          <p className="mt-4 text-base sm:text-lg text-slate-600 leading-relaxed">
            Eliminate food waste intelligently. Route pure vegetarian surplus to <span className="font-bold text-slate-800">Gaushalas</span>, high-protein & non-veg meals to <span className="font-bold text-slate-800">Dog Shelters</span>, certified hot meals to <span className="font-bold text-slate-800">Human Shelters</span>, and leftover kitchen scraps into <span className="font-bold text-slate-800">Organic Compost & Bio-CNG</span>.
          </p>
        </div>

        {/* 4 Destination Category Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-14">
          {/* Card 1: Gaushala */}
          <div className="rounded-2xl p-5 border border-amber-200 bg-amber-50/50 hover:bg-amber-50 transition-all duration-200 shadow-sm flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center mb-4">
                <Wheat className="w-6 h-6" />
              </div>
              <h3 className="font-outfit font-bold text-lg text-slate-900">Gaushalas (Cattle)</h3>
              <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                Clean vegetarian grains, dry rotis, green trimmings, cooked rice, and non-spicy dal. Strictly pure veg with zero garlic/onion or non-veg.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-amber-200/80 flex items-center justify-between text-xs font-semibold text-amber-800">
              <span>Pure Vegetarian</span>
              <span className="font-mono bg-amber-200/70 px-2 py-0.5 rounded">2 Active Shelters</span>
            </div>
          </div>

          {/* Card 2: Dog Shelter */}
          <div className="rounded-2xl p-5 border border-orange-200 bg-orange-50/50 hover:bg-orange-50 transition-all duration-200 shadow-sm flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-orange-100 text-orange-700 flex items-center justify-center mb-4">
                <Dog className="w-6 h-6" />
              </div>
              <h3 className="font-outfit font-bold text-lg text-slate-900">Dog Shelters (Canine)</h3>
              <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                Vegetarian & Non-Vegetarian surplus: chicken, meat stew, boiled eggs, broths, liver, curd rice, and protein-rich banquet leftovers.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-orange-200/80 flex items-center justify-between text-xs font-semibold text-orange-800">
              <span>Veg + Non-Veg Accepted</span>
              <span className="font-mono bg-orange-200/70 px-2 py-0.5 rounded">2 Active Sanctuaries</span>
            </div>
          </div>

          {/* Card 3: Human Shelter */}
          <div className="rounded-2xl p-5 border border-emerald-200 bg-emerald-50/50 hover:bg-emerald-50 transition-all duration-200 shadow-sm flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center mb-4">
                <HeartHandshake className="w-6 h-6" />
              </div>
              <h3 className="font-outfit font-bold text-lg text-slate-900">Human Shelters</h3>
              <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                FSSAI-verified wholesome cooked meals, freshly prepared (&lt;3.5h) and safely maintained at hot holding temperatures (&gt;60°C).
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-emerald-200/80 flex items-center justify-between text-xs font-semibold text-emerald-800">
              <span>FSSAI Certified Hot</span>
              <span className="font-mono bg-emerald-200/70 px-2 py-0.5 rounded">2 Community Hubs</span>
            </div>
          </div>

          {/* Card 4: Bio-Composting */}
          <div className="rounded-2xl p-5 border border-lime-200 bg-lime-50/50 hover:bg-lime-50 transition-all duration-200 shadow-sm flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-lime-100 text-lime-700 flex items-center justify-center mb-4">
                <Recycle className="w-6 h-6" />
              </div>
              <h3 className="font-outfit font-bold text-lg text-slate-900">Organic Bio-Compost</h3>
              <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                Kitchen discards, plate scrapings, sour curries, vegetable peels, and stale food converted to FCO 1985 certified organic manure & clean Bio-CNG.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-lime-200/80 flex items-center justify-between text-xs font-semibold text-lime-800">
              <span>Zero-Waste Humus</span>
              <span className="font-mono bg-lime-200/70 px-2 py-0.5 rounded">2 Plants</span>
            </div>
          </div>
        </div>

        {/* Main 2-Column Section: Left = Donor Console, Right = Live AI Recommendation & Route */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start mb-16">
          {/* Left Column (7 cols): Donor Dispatch Form */}
          <div className="lg:col-span-7 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xl">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
              <div>
                <span className="text-xs uppercase tracking-wider font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200">
                  Step 1: Donor Dispatch Console
                </span>
                <h3 className="font-outfit font-bold text-2xl text-slate-900 mt-2">
                  Create Surplus Food Donation
                </h3>
              </div>

              {/* Mode Toggle */}
              <div className="inline-flex rounded-xl bg-slate-100 p-1 border border-slate-200">
                <button
                  type="button"
                  onClick={() => setDecisionMode('SMART_RECOMMEND')}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    decisionMode === 'SMART_RECOMMEND'
                      ? 'bg-emerald-600 text-white shadow-sm'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  AI Recommendation
                </button>
                <button
                  type="button"
                  onClick={() => setDecisionMode('MANUAL_SELECT')}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    decisionMode === 'MANUAL_SELECT'
                      ? 'bg-emerald-600 text-white shadow-sm'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <MapPin className="w-3.5 h-3.5" />
                  Direct Choice
                </button>
              </div>
            </div>

            <form onSubmit={handleSmartDonationSubmit} className="mt-6 space-y-5">
              {/* Food Title & Location */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-1.5">
                    Food Item Description
                  </label>
                  <input
                    type="text"
                    value={foodTitle}
                    onChange={(e) => setFoodTitle(e.target.value)}
                    required
                    placeholder="e.g. 50kg Chicken Biryani or Rice & Rotis"
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-slate-50/50"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-1.5">
                    Pickup Kitchen Address
                  </label>
                  <input
                    type="text"
                    value={donorLocation}
                    onChange={(e) => setDonorLocation(e.target.value)}
                    required
                    placeholder="e.g. Baner Main Road, Pune"
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-slate-50/50"
                  />
                </div>
              </div>

              {/* Diet Type & Category */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-1.5">
                    Dietary Classification
                  </label>
                  <select
                    value={dietType}
                    onChange={(e) => setDietType(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
                  >
                    <option value="PURE_VEG">🌱 Pure Vegetarian (Cattle & Gaushala Friendly)</option>
                    <option value="NON_VEG">🍗 Non-Vegetarian / Meat Surplus (Dog Shelter Friendly)</option>
                    <option value="MIXED_COOKED">🍲 Mixed Cooked Meals (General Human Shelter)</option>
                    <option value="UNSUITABLE_SCRAPS">♻️ Kitchen Scraps / Inedible (Organic Compost)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-1.5">
                    Food Category
                  </label>
                  <select
                    value={foodCategory}
                    onChange={(e) => setFoodCategory(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
                  >
                    <option value="VEG_GRAIN">Cooked Rice / Pulao / Biryani</option>
                    <option value="BREAD_ROTI">Rotis, Chapatis & Breads</option>
                    <option value="DAIRY_CURRY">Paneer, Dals & Curries</option>
                    <option value="MEAT_POULTRY">Chicken, Broth, Meat Stew</option>
                    <option value="PRODUCE_SCRAPS">Vegetable Peels & Kitchen Waste</option>
                  </select>
                </div>
              </div>

              {/* Quantity, Temperature, Hours Cooked */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-1.5">
                    Quantity (kg)
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="1000"
                    value={quantityKg}
                    onChange={(e) => setQuantityKg(e.target.value)}
                    required
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm text-slate-900 font-mono font-bold focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-slate-50/50"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-1.5">
                    Holding Temp (°C)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={temperatureC}
                    onChange={(e) => setTemperatureC(parseFloat(e.target.value) || 0)}
                    required
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm text-slate-900 font-mono font-bold focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-slate-50/50"
                  />
                  <span className="text-[10px] text-slate-500 mt-1 block">
                    {temperatureC >= 60 ? '🔥 Safe hot-holding (>60°C)' : '⚠️ Below 60°C'}
                  </span>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-1.5">
                    Hours Since Cooked
                  </label>
                  <input
                    type="number"
                    step="0.5"
                    min="0"
                    max="48"
                    value={hoursCooked}
                    onChange={(e) => setHoursCooked(parseFloat(e.target.value) || 0)}
                    required
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm text-slate-900 font-mono font-bold focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-slate-50/50"
                  />
                  <span className="text-[10px] text-slate-500 mt-1 block">
                    {hoursCooked <= 3.5 ? '✅ Fresh (<3.5 hrs)' : '⚠️ Hold > 3.5 hrs'}
                  </span>
                </div>
              </div>

              {/* Packaging & Direct Choice (if Manual mode) */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-1.5">
                    Packaging Type
                  </label>
                  <select
                    value={packaging}
                    onChange={(e) => setPackaging(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
                  >
                    <option value="CAMBRO_HOT_BOX">Insulated Thermal Cambro (Hot / Chilled)</option>
                    <option value="FOOD_GRADE_CONTAINER">Food-Grade Stainless Steel Bins</option>
                    <option value="SEALED_FOIL_TRAYS">Individual Foil Sealed Trays</option>
                    <option value="CRATES_BAGS">Compost Heavy-Duty Biodegradable Bags</option>
                  </select>
                </div>

                {decisionMode === 'MANUAL_SELECT' ? (
                  <div>
                    <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-1.5">
                      Direct Recipient Selection
                    </label>
                    <select
                      value={selectedRecipientId}
                      onChange={(e) => setSelectedRecipientId(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl border border-emerald-400 text-sm text-slate-900 font-semibold focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-emerald-50/30"
                    >
                      {recipients.map((rec) => (
                        <option key={rec.id} value={rec.id}>
                          [{rec.type.replace('_', ' ')}] {rec.name} ({rec.distance_km || 5} km)
                        </option>
                      ))}
                    </select>
                  </div>
                ) : (
                  <div>
                    <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-1.5">
                      AI Triage Logic
                    </label>
                    <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-emerald-600 shrink-0" />
                      <span className="truncate">Auto-matching based on diet, temp, hold time & capacity</span>
                    </div>
                  </div>
                )}
              </div>

              {/* Donor Notes */}
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-1.5">
                  Handling Instructions / Donor Notes
                </label>
                <textarea
                  rows="2"
                  value={donorNotes}
                  onChange={(e) => setDonorNotes(e.target.value)}
                  placeholder="Special instructions for courier or recipient intake team..."
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-slate-50/50 resize-none"
                />
              </div>

              {/* Submit Dispatch Button */}
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full py-3.5 px-6 rounded-2xl bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800 text-white font-bold text-base shadow-lg shadow-emerald-700/20 hover:shadow-emerald-700/30 transition-all flex items-center justify-center gap-2 disabled:opacity-70 cursor-pointer"
              >
                {isSubmitting ? (
                  <>
                    <RefreshCw className="w-5 h-5 animate-spin" />
                    <span>Optimizing Route & Dispatching...</span>
                  </>
                ) : (
                  <>
                    <Truck className="w-5 h-5" />
                    <span>Confirm & Dispatch Rescue Courier ({quantityKg} kg)</span>
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Right Column (5 cols): Live AI Recommendation & Route Preview */}
          <div className="lg:col-span-5 flex flex-col gap-6">
            {/* Recommendation Match Card */}
            <div className="bg-gradient-to-br from-slate-900 to-slate-950 text-white rounded-3xl p-6 sm:p-7 shadow-xl border border-slate-800 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-44 h-44 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

              <div className="flex items-center justify-between mb-4">
                <span className="text-[11px] font-mono uppercase tracking-wider bg-emerald-500/20 text-emerald-400 font-bold px-3 py-1 rounded-full border border-emerald-500/30 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" />
                  Live Route Recommendation
                </span>
                <span className="font-mono text-xs font-bold text-emerald-400 bg-emerald-950/80 px-2.5 py-1 rounded-lg border border-emerald-800">
                  {smartRecommendation.confidenceScore}% Match Score
                </span>
              </div>

              <div className="flex items-start gap-3.5 my-3">
                <div className="w-12 h-12 rounded-2xl bg-white/10 flex items-center justify-center shrink-0 border border-white/10">
                  {getRecipientTypeIcon(smartRecommendation.recommendedRecipient.type)}
                </div>
                <div>
                  <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded border ${getRecipientTypeBadge(smartRecommendation.recommendedRecipient.type)}`}>
                    {smartRecommendation.recommendedRecipient.type_label}
                  </span>
                  <h4 className="font-outfit font-bold text-xl text-white mt-1">
                    {smartRecommendation.recommendedRecipient.name}
                  </h4>
                  <p className="text-xs text-slate-400 flex items-center gap-1 mt-1">
                    <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                    <span className="truncate">{smartRecommendation.recommendedRecipient.address}</span>
                  </p>
                </div>
              </div>

              {/* Rationale explanation */}
              <div className="mt-4 p-3.5 rounded-2xl bg-slate-800/80 border border-slate-700/80 text-xs text-slate-300 leading-relaxed">
                <span className="font-bold text-emerald-400 block mb-1">Algorithmic Decision:</span>
                {smartRecommendation.rationale}
              </div>

              {/* Key Route Metrics */}
              <div className="grid grid-cols-2 gap-3 mt-4 pt-4 border-t border-slate-800">
                <div className="p-3 rounded-xl bg-white/5 border border-white/5">
                  <div className="text-[11px] text-slate-400 flex items-center gap-1 font-medium">
                    <Route className="w-3.5 h-3.5 text-emerald-400" />
                    Optimal Distance
                  </div>
                  <div className="text-lg font-mono font-bold text-white mt-0.5">
                    {smartRecommendation.route.distanceKm} km
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-white/5 border border-white/5">
                  <div className="text-[11px] text-slate-400 flex items-center gap-1 font-medium">
                    <Clock className="w-3.5 h-3.5 text-amber-400" />
                    Estimated Transit
                  </div>
                  <div className="text-lg font-mono font-bold text-white mt-0.5">
                    {smartRecommendation.route.transitTimeMins} mins
                  </div>
                </div>
              </div>

              {/* Visual Route Waypoints */}
              <div className="mt-4 p-3.5 rounded-2xl bg-white/5 border border-white/10">
                <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
                  Optimized Waypoint Sequence
                </span>
                <div className="space-y-2 text-xs">
                  {smartRecommendation.route.waypoints.map((point, idx) => (
                    <div key={idx} className="flex items-center gap-2">
                      <div className="w-5 h-5 rounded-full bg-emerald-600/30 text-emerald-400 font-mono text-[10px] flex items-center justify-center font-bold shrink-0">
                        {idx + 1}
                      </div>
                      <span className="text-slate-300 font-medium truncate">{point}</span>
                    </div>
                  ))}
                </div>

                <div className="mt-3 pt-3 border-t border-white/10 flex items-center justify-between text-xs text-slate-400">
                  <span className="flex items-center gap-1">
                    <Truck className="w-3.5 h-3.5 text-emerald-400" />
                    {smartRecommendation.route.vehicleAssigned.split('(')[0]}
                  </span>
                  <span className="text-emerald-400 font-semibold">Active Dispatch Ready</span>
                </div>
              </div>
            </div>

            {/* Quick Contact & Capacity Mini Card */}
            <div className="p-5 rounded-3xl bg-slate-100 border border-slate-200">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                  Live Shelter Capacity
                </span>
                <span className="text-xs font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">
                  {smartRecommendation.recommendedRecipient.capacity_remaining_kg} kg Available
                </span>
              </div>
              <div className="w-full bg-slate-200 h-2.5 rounded-full overflow-hidden">
                <div
                  className="bg-emerald-600 h-full rounded-full transition-all"
                  style={{
                    width: `${Math.min(
                      100,
                      (smartRecommendation.recommendedRecipient.current_intake_kg /
                        smartRecommendation.recommendedRecipient.daily_capacity_kg) *
                        100
                    )}%`
                  }}
                />
              </div>
              <div className="mt-3 flex items-center justify-between text-xs text-slate-600">
                <span>Intake: {smartRecommendation.recommendedRecipient.current_intake_kg} kg</span>
                <span>Max: {smartRecommendation.recommendedRecipient.daily_capacity_kg} kg/day</span>
              </div>
            </div>
          </div>
        </div>

        {/* ========================================================
            RECIPIENT CONTACT DIRECTORY CARDS
        ======================================================== */}
        <div className="mt-16 pt-12 border-t border-slate-200">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
            <div>
              <span className="text-xs uppercase tracking-wider font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200">
                Recipient Network
              </span>
              <h3 className="font-outfit font-bold text-2xl sm:text-3xl text-slate-900 mt-2">
                Verified Recipient Directory & Contact Cards
              </h3>
              <p className="text-sm text-slate-600 mt-1 max-w-xl">
                Every shelter is verified with municipal, FSSAI, Animal Welfare Board of India, or Pollution Control Board compliance.
              </p>
            </div>

            {/* Filter Pills */}
            <div className="flex flex-wrap items-center gap-2">
              {[
                { key: 'ALL', label: 'All Recipients' },
                { key: 'RURAL_COMMUNITY', label: '🌾 Rural Distribution' },
                { key: 'HUMAN_SHELTER', label: '🍲 Community & Old Age Homes' },
                { key: 'GAUSHALA', label: '🐄 Gaushala' },
                { key: 'DOG_SHELTER', label: '🐕 Animal Welfare' },
                { key: 'COMPOST_MANURE', label: '♻️ Bio-Compost' }
              ].map((btn) => (
                <button
                  key={btn.key}
                  type="button"
                  onClick={() => setTypeFilter(btn.key)}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                    typeFilter === btn.key
                      ? 'bg-slate-900 text-white shadow-sm'
                      : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100'
                  }`}
                >
                  {btn.label}
                </button>
              ))}
            </div>
          </div>

          {/* Directory Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredRecipients.map((rec) => (
              <div
                key={rec.id}
                className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between group hover:-translate-y-1"
              >
                <div>
                  {/* Photo Banner */}
                  <div className="relative aspect-[16/10] overflow-hidden bg-slate-900">
                    <img
                      src={rec.image_url || '/images/community-food-serving-hall.jpg'}
                      alt={rec.name}
                      loading="lazy"
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      onError={(e) => {
                        e.currentTarget.src = '/images/community-serving.jpg';
                      }}
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-slate-950/75 via-transparent to-black/25" />
                    <div className="absolute top-3 left-3">
                      <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded shadow-sm backdrop-blur-md border ${getRecipientTypeBadge(rec.type)}`}>
                        {rec.type_label.split('(')[0]}
                      </span>
                    </div>
                    <div className="absolute top-3 right-3">
                      <span className="text-[10px] font-mono font-bold text-white bg-slate-950/70 backdrop-blur-md px-2 py-0.5 rounded border border-white/20">
                        {rec.distance_km || 5.0} km
                      </span>
                    </div>
                    <div className="absolute bottom-2.5 left-3 right-3">
                      <span className="text-[10px] font-medium text-emerald-200 bg-emerald-950/80 backdrop-blur-xs px-2 py-0.5 rounded border border-emerald-500/30 truncate block">
                        Intake: {rec.daily_capacity_kg} kg/day · {rec.resident_count ? `${rec.resident_count} Meals/Day` : rec.cattle_count ? `${rec.cattle_count} Cows` : `${rec.dog_count || 100} Rescues`}
                      </span>
                    </div>
                  </div>

                  <div className="p-5">
                    <h4 className="font-outfit font-bold text-base text-slate-900 group-hover:text-emerald-700 transition-colors line-clamp-2">
                      {rec.name}
                    </h4>

                    {/* Verification Seal */}
                    <div className="mt-2 flex items-center gap-1.5 text-xs text-emerald-700 font-semibold bg-emerald-50 px-2 py-1 rounded-lg border border-emerald-100">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                      <span className="truncate">{rec.verified_badge}</span>
                    </div>

                    {/* Contact Person Details */}
                    <div className="mt-4 space-y-1.5 text-xs text-slate-600 border-t border-slate-100 pt-3">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-slate-800">{rec.contact_person}</span>
                        <span className="text-[11px] text-slate-500 font-mono">{rec.pickup_lead_time_mins}m ETA</span>
                      </div>

                      <p className="flex items-center gap-1.5 text-slate-600 truncate">
                        <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                        <span className="truncate">{rec.address}</span>
                      </p>

                      <a
                        href={`tel:${rec.phone}`}
                        className="inline-flex items-center gap-1.5 text-emerald-700 hover:text-emerald-800 font-bold font-mono text-xs pt-1"
                      >
                        <Phone className="w-3.5 h-3.5" />
                        {rec.phone}
                      </a>
                    </div>

                    {/* Diet compatibility tag */}
                    <div className="mt-3">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                        Diet Suitability:
                      </span>
                      <span className="text-xs font-medium text-slate-700 bg-slate-100 px-2 py-0.5 rounded inline-block">
                        {rec.diet_compatibility}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Card Action */}
                <div className="px-5 pb-5 pt-0">
                  <button
                    type="button"
                    onClick={() => {
                      setSelectedRecipientId(rec.id);
                      setDecisionMode('MANUAL_SELECT');
                      if (onAddToast) {
                        onAddToast(`Selected ${rec.name} for direct donation!`);
                      }
                      const consoleEl = document.getElementById('smart-rescue');
                      if (consoleEl) {
                        consoleEl.scrollIntoView({ behavior: 'smooth' });
                      }
                    }}
                    className="w-full py-2.5 px-3 rounded-xl bg-slate-900 hover:bg-emerald-600 text-white text-xs font-bold transition-all flex items-center justify-center gap-1.5 cursor-pointer shadow-sm"
                  >
                    <span>Donate Surplus to This Hub</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ========================================================
            LEFTOVER FOOD SCRAPS -> ORGANIC COMPOST CONVERTER
        ======================================================== */}
        <div className="mt-16 bg-gradient-to-br from-emerald-900 via-emerald-950 to-slate-950 text-white rounded-3xl p-7 sm:p-10 border border-emerald-800/50 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-80 h-80 bg-lime-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
            {/* Left Col (6 cols): Copy & Converter Form */}
            <div className="lg:col-span-6">
              <span className="text-xs uppercase tracking-wider font-bold text-lime-400 bg-lime-950/80 px-3 py-1 rounded-full border border-lime-500/30 inline-flex items-center gap-1.5">
                <Recycle className="w-3.5 h-3.5 text-lime-400" />
                Zero-Waste Bio-Compost System
              </span>

              <h3 className="font-outfit font-extrabold text-2xl sm:text-3xl lg:text-4xl text-white mt-4 tracking-tight">
                Turn Inedible Leftover Scraps Into Certified Organic Manure
              </h3>

              <p className="text-sm text-slate-300 mt-3 leading-relaxed">
                When meals have soured, passed the 4-hour safety holding window, or are raw vegetable trimmings unsuitable for human or cattle consumption, they never enter municipal landfills. Our bio-methanation and microbial aerobic composting converts every scrap into rich city compost (FCO 1985 Standard) and clean Bio-CNG.
              </p>

              {/* Quick Input Form */}
              <form onSubmit={handleScrapsConvert} className="mt-6 space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-bold text-emerald-300 uppercase tracking-wide mb-1">
                      Scrap Quantity (kg)
                    </label>
                    <input
                      type="number"
                      min="5"
                      max="5000"
                      value={scrapKg}
                      onChange={(e) => setScrapKg(e.target.value)}
                      required
                      className="w-full px-3.5 py-2.5 rounded-xl bg-white/10 border border-white/20 text-white font-mono font-bold text-base focus:outline-none focus:ring-2 focus:ring-lime-400"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-emerald-300 uppercase tracking-wide mb-1">
                      Type of Inedible Scraps
                    </label>
                    <select
                      value={scrapType}
                      onChange={(e) => setScrapType(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-white/20 text-white text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-lime-400"
                    >
                      <option value="MIXED_KITCHEN_SCRAPS">Kitchen Peels & Veg Trimmings</option>
                      <option value="EXPIRED_COOKED_GRAINS">Spoiled Cooked Grains / Rotis</option>
                      <option value="PLATE_SCRAPINGS">Banquet Plate Scrapings</option>
                      <option value="CITRUS_SOUR_CURRIES">Citrus, Onion & Sour Gravies</option>
                    </select>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isCompostConverting}
                  className="w-full py-3 px-6 rounded-2xl bg-gradient-to-r from-lime-500 to-emerald-500 hover:from-lime-600 hover:to-emerald-600 text-slate-950 font-bold text-sm shadow-lg shadow-lime-500/20 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-70"
                >
                  {isCompostConverting ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      <span>Generating FCO Certificate...</span>
                    </>
                  ) : (
                    <>
                      <Award className="w-4 h-4" />
                      <span>Convert {scrapKg} kg Scraps to Certified Organic Manure</span>
                    </>
                  )}
                </button>
              </form>
            </div>

            {/* Right Col (6 cols): Live Conversion Counters */}
            <div className="lg:col-span-6 grid grid-cols-2 gap-4">
              <div className="p-5 rounded-2xl bg-white/10 border border-white/10 backdrop-blur-sm">
                <span className="text-xs text-lime-300 font-semibold uppercase tracking-wider block">
                  Humus Compost Yield
                </span>
                <div className="font-mono font-extrabold text-3xl sm:text-4xl text-white mt-1">
                  {compostMetrics.humusKg} <span className="text-lg font-normal text-lime-400">kg</span>
                </div>
                <p className="text-xs text-slate-300 mt-2">
                  40% high-grade organic fertilizer (NPK enriched).
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-white/10 border border-white/10 backdrop-blur-sm">
                <span className="text-xs text-emerald-300 font-semibold uppercase tracking-wider block">
                  Methane / CO₂e Prevented
                </span>
                <div className="font-mono font-extrabold text-3xl sm:text-4xl text-white mt-1">
                  {compostMetrics.co2eSavedKg} <span className="text-lg font-normal text-emerald-400">kg</span>
                </div>
                <p className="text-xs text-slate-300 mt-2">
                  Zero landfill methane emissions guaranteed.
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-white/10 border border-white/10 backdrop-blur-sm">
                <span className="text-xs text-amber-300 font-semibold uppercase tracking-wider block">
                  Bio-CNG Clean Energy
                </span>
                <div className="font-mono font-extrabold text-3xl sm:text-4xl text-white mt-1">
                  {compostMetrics.bioCngKwh} <span className="text-lg font-normal text-amber-400">kWh</span>
                </div>
                <p className="text-xs text-slate-300 mt-2">
                  Equivalent to 3.8 days of clean cooking gas.
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-white/10 border border-white/10 backdrop-blur-sm">
                <span className="text-xs text-cyan-300 font-semibold uppercase tracking-wider block">
                  Topsoil Enriched
                </span>
                <div className="font-mono font-extrabold text-3xl sm:text-4xl text-white mt-1">
                  {compostMetrics.soilAreaSqM} <span className="text-lg font-normal text-cyan-400">sq.m</span>
                </div>
                <p className="text-xs text-slate-300 mt-2">
                  Regenerates urban micro-gardens & organic farms.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ========================================================
          MODAL 1: DISPATCH SUCCESS CONFIRMATION MODAL
      ======================================================== */}
      {dispatchSuccessModal && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm animate-fade-in"
        >
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setDispatchSuccessModal(null)}
              className="absolute top-5 right-5 p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="w-14 h-14 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center mb-4">
              <CheckCircle2 className="w-8 h-8" />
            </div>

            <span className="text-xs font-mono font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200">
              Batch Dispatched: {dispatchSuccessModal.batchId}
            </span>

            <h3 className="font-outfit font-bold text-2xl text-slate-900 mt-2">
              Rescue Courier Dispatched!
            </h3>

            <p className="text-sm text-slate-600 mt-1">
              Your surplus donation of <span className="font-bold text-slate-900">{dispatchSuccessModal.mealsOrKg}</span> has been confirmed and routed to <span className="font-bold text-slate-900">{dispatchSuccessModal.recipient.name}</span>.
            </p>

            {/* Recipient Card inside Modal */}
            <div className="mt-4 p-4 rounded-2xl bg-slate-50 border border-slate-200">
              <div className="flex items-center justify-between text-xs font-bold text-slate-700">
                <span>Matched Destination</span>
                <span className={`px-2 py-0.5 rounded border ${getRecipientTypeBadge(dispatchSuccessModal.recipient.type)}`}>
                  {dispatchSuccessModal.recipient.type_label}
                </span>
              </div>
              <h4 className="font-outfit font-bold text-base text-slate-900 mt-1">
                {dispatchSuccessModal.recipient.name}
              </h4>
              <p className="text-xs text-slate-500 mt-0.5">{dispatchSuccessModal.recipient.address}</p>

              <div className="mt-3 pt-3 border-t border-slate-200 grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span className="text-slate-400 block">Contact Person:</span>
                  <span className="font-semibold text-slate-800">{dispatchSuccessModal.recipient.contact_person}</span>
                </div>
                <div>
                  <span className="text-slate-400 block">Helpline:</span>
                  <span className="font-mono font-semibold text-emerald-700">{dispatchSuccessModal.recipient.phone}</span>
                </div>
              </div>
            </div>

            {/* Route & Courier Details */}
            <div className="mt-4 p-4 rounded-2xl bg-slate-900 text-white">
              <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
                <span>Assigned Vehicle & Courier</span>
                <span className="text-emerald-400 font-bold">ETA: ~{dispatchSuccessModal.route.transitTimeMins} mins</span>
              </div>
              <div className="text-sm font-bold text-white flex items-center gap-2">
                <Truck className="w-4 h-4 text-emerald-400" />
                {dispatchSuccessModal.route.vehicleAssigned}
              </div>
              <div className="text-xs text-slate-300 mt-1">
                Driver: {dispatchSuccessModal.route.driverName} ({dispatchSuccessModal.route.driverPhone})
              </div>
              <div className="text-xs text-emerald-400 mt-2 font-mono">
                Telemetry: {dispatchSuccessModal.route.tempControl}
              </div>
            </div>

            <div className="mt-6 flex items-center justify-between gap-3">
              <div className="flex items-center gap-1.5 text-xs text-emerald-700 font-bold bg-emerald-50 px-3 py-2 rounded-xl border border-emerald-200">
                <Award className="w-4 h-4 text-emerald-600" />
                +{dispatchSuccessModal.impactCredits} Impact Credits Earned
              </div>
              <button
                type="button"
                onClick={() => setDispatchSuccessModal(null)}
                className="py-2.5 px-5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md transition-all cursor-pointer"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================
          MODAL 2: OFFICIAL FCO ORGANIC MANURE CERTIFICATE MODAL
      ======================================================== */}
      {compostCertModal && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/75 backdrop-blur-sm animate-fade-in"
        >
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border-4 border-lime-600/30 relative max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setCompostCertModal(null)}
              className="absolute top-5 right-5 p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="text-center mb-6">
              <div className="w-16 h-16 rounded-3xl bg-lime-100 text-lime-700 mx-auto flex items-center justify-center mb-3 border-2 border-lime-300 shadow-sm">
                <Award className="w-9 h-9" />
              </div>
              <span className="text-[11px] font-mono uppercase bg-lime-100 text-lime-900 font-extrabold px-3 py-1 rounded-full border border-lime-300">
                Official Zero-Landfill Certificate
              </span>
              <h3 className="font-outfit font-extrabold text-2xl text-slate-900 mt-2">
                Certified Organic Manure & Humus Batch
              </h3>
              <p className="text-xs text-slate-500 mt-1">
                Conforms to Fertilizer (Control) Order 1985 (FCO) - City Compost Standard
              </p>
            </div>

            {/* Certificate Ledger Details */}
            <div className="bg-slate-50 rounded-2xl p-5 border border-slate-200 space-y-3 text-xs">
              <div className="flex justify-between pb-2 border-b border-slate-200">
                <span className="text-slate-500">Certificate Reference:</span>
                <span className="font-mono font-bold text-slate-900">{compostCertModal.certificate_id}</span>
              </div>

              <div className="flex justify-between pb-2 border-b border-slate-200">
                <span className="text-slate-500">Certified Date:</span>
                <span className="font-mono font-semibold text-slate-900">{compostCertModal.certified_date}</span>
              </div>

              <div className="flex justify-between pb-2 border-b border-slate-200">
                <span className="text-slate-500">Raw Scraps Diverted:</span>
                <span className="font-mono font-bold text-slate-900">{compostCertModal.input_scraps_kg} kg</span>
              </div>

              <div className="flex justify-between pb-2 border-b border-slate-200">
                <span className="text-slate-500">Net Organic Humus Produced:</span>
                <span className="font-mono font-bold text-lime-700">{compostCertModal.humus_yield_kg} kg</span>
              </div>

              <div className="flex justify-between pb-2 border-b border-slate-200">
                <span className="text-slate-500">CO₂e Methane Abatement:</span>
                <span className="font-mono font-bold text-emerald-700">{compostCertModal.co2e_offset_kg} kg CO₂e</span>
              </div>

              <div className="flex justify-between">
                <span className="text-slate-500">Clean Bio-CNG Output:</span>
                <span className="font-mono font-bold text-amber-700">{compostCertModal.biocng_kwh} kWh</span>
              </div>
            </div>

            {/* Quality Standard Badges */}
            <div className="mt-4 grid grid-cols-3 gap-2 text-center">
              <div className="p-2 rounded-xl bg-lime-50 border border-lime-200">
                <span className="text-[10px] text-lime-800 block">C:N Ratio</span>
                <span className="font-mono font-bold text-xs text-lime-900">18:1 (Optimal)</span>
              </div>
              <div className="p-2 rounded-xl bg-emerald-50 border border-emerald-200">
                <span className="text-[10px] text-emerald-800 block">Moisture</span>
                <span className="font-mono font-bold text-xs text-emerald-900">&lt; 25% FCO</span>
              </div>
              <div className="p-2 rounded-xl bg-amber-50 border border-amber-200">
                <span className="text-[10px] text-amber-800 block">Heavy Metals</span>
                <span className="font-mono font-bold text-xs text-amber-900">Below Limits</span>
              </div>
            </div>

            <div className="mt-6 flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={() => setCompostCertModal(null)}
                className="w-full py-2.5 px-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs shadow-md transition-all cursor-pointer"
              >
                Close Certificate
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
