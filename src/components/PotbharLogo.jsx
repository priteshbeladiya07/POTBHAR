import React from 'react';

/**
 * Official POTBHAR Circular Logo Component
 * - Green Heart at top apex
 * - Green Leafy Sprouts arching the top
 * - Saffron / Golden Pot (Handi) with rim & inner white opening
 * - White circular badge with Green Checkmark in center
 * - Earth-brown cupping hand underneath sweeping into a circular recycling arrow
 */
export default function PotbharLogo({ className = "w-11 h-11", size }) {
  const style = size ? { width: size, height: size } : undefined;

  return (
    <div className={`relative flex items-center justify-center shrink-0 ${className}`} style={style}>
      <svg
        viewBox="34 18 136 148"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full select-none"
      >
        {/* Soft Warm Circular Backdrop */}
        <circle cx="102" cy="92" r="70" fill="#FFF9EF" />

        {/* ========================================================
            1. TOP: GREEN LEAVES & APEX HEART
        ======================================================== */}
        {/* Heart at Top Apex */}
        <path
          d="M100 44 C95 38 86 31 88 24 C90 17 98 17 100 22 C102 17 110 17 112 24 C114 31 105 38 100 44 Z"
          fill="#2D8A4E"
        />

        {/* Left Sweeping Green Arch / Vine */}
        <path
          d="M48 106 C42 85 48 58 70 42 C82 33 93 30 100 30"
          stroke="#2D8A4E"
          strokeWidth="9"
          strokeLinecap="round"
        />

        {/* Right Sweeping Green Arch */}
        <path
          d="M100 30 C115 30 136 38 148 55 C156 67 158 82 154 98"
          stroke="#2D8A4E"
          strokeWidth="9"
          strokeLinecap="round"
        />

        {/* Prominent Left Sprout Leaf */}
        <path
          d="M62 65 C50 46 72 34 89 44 C76 52 70 60 62 65 Z"
          fill="#2D8A4E"
        />
        {/* Leaf Vein highlight */}
        <path
          d="M66 60 C73 54 81 48 85 46"
          stroke="#FFF9EF"
          strokeWidth="2"
          strokeLinecap="round"
        />

        {/* Secondary Inner Leaf Sprout */}
        <path
          d="M97 68 C94 51 112 50 118 64 C109 63 103 66 97 68 Z"
          fill="#2D8A4E"
        />

        {/* ========================================================
            2. BOTTOM: DARK BROWN HAND CRADLING POT & CIRCULAR ARROW
        ======================================================== */}
        {/* The Earth-Brown Hand sweeping into circular arrow */}
        <path
          d="M44 95 C40 108 40 122 47 134 C58 152 78 163 100 163 C118 163 138 153 150 138 C155 131 157 124 158 116"
          stroke="#34251D"
          strokeWidth="11"
          strokeLinecap="round"
        />

        {/* Cradling Hand Palm & Gentle Fingers under the Pot */}
        <path
          d="M68 135 C78 143 92 147 106 146 C115 145 120 142 124 139 C121 146 112 153 100 153 C86 153 74 146 68 135 Z"
          fill="#34251D"
        />
        <path
          d="M74 133 C84 140 96 143 110 141 C115 140 119 137 121 135 C116 142 105 146 95 146 C83 146 76 139 74 133 Z"
          fill="#FFF9EF"
        />

        {/* Upward Circular Arrowhead at Right */}
        <path
          d="M141 122 L158 101 L173 124 L162 121 L158 126 L153 121 Z"
          fill="#34251D"
          strokeLinejoin="round"
        />

        {/* ========================================================
            3. CENTER: ORANGE / SAFFRON HANDI (POT)
        ======================================================== */}
        {/* Pot Body */}
        <path
          d="M58 92 C56 104 60 120 73 131 C81 137 90 140 100 140 C110 140 119 137 127 131 C140 120 144 104 142 92 Z"
          fill="#EB7D1E"
        />

        {/* Pot Outer Rounded Lip / Rim */}
        <rect
          x="53"
          y="83"
          width="94"
          height="13"
          rx="6.5"
          fill="#EB7D1E"
        />

        {/* Inner Opening of the Pot */}
        <ellipse
          cx="100"
          cy="89.5"
          rx="38"
          ry="5"
          fill="#FFF9EF"
        />

        {/* Left Glossy Curved Highlight on Pot Body */}
        <path
          d="M64 99 C62 108 65 119 72 126"
          stroke="#FFF9EF"
          strokeWidth="4"
          strokeLinecap="round"
          strokeOpacity="0.95"
        />

        {/* ========================================================
            4. CENTER BADGE: WHITE DISC WITH GREEN CHECKMARK
        ======================================================== */}
        {/* White Circular Seal in Pot Center */}
        <circle
          cx="100"
          cy="114"
          r="13"
          fill="#FFFFFF"
        />

        {/* Green Verified Checkmark inside the White Disc */}
        <path
          d="M93.5 114 L98 118.5 L107.5 108"
          fill="none"
          stroke="#2D8A4E"
          strokeWidth="3.4"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
}
