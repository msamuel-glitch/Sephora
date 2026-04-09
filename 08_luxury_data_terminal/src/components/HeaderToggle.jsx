import { motion } from 'framer-motion';

export default function HeaderToggle({ isNocibe, setIsNocibe }) {
  return (
    <div className="flex items-center gap-4">
      <button
        onClick={() => setIsNocibe(false)}
        className={`
          font-data text-[0.65rem] uppercase tracking-[0.15em] px-5 py-2.5 rounded-full
          transition-all duration-300 cursor-pointer border
          ${!isNocibe
            ? 'text-primaryText bg-white shadow-lift border-black/5'
            : 'text-tertiaryText bg-transparent border-black/5 hover:text-secondaryText hover:border-black/10'
          }
        `}
      >
        Sephora Intelligence
      </button>

      <div className="w-px h-5 bg-black/10" />

      <button
        onClick={() => setIsNocibe(true)}
        className={`
          font-data text-[0.65rem] uppercase tracking-[0.15em] px-5 py-2.5 rounded-full
          transition-all duration-300 cursor-pointer border
          ${isNocibe
            ? 'text-primaryText bg-white shadow-lift border-black/10'
            : 'text-tertiaryText bg-transparent border-black/5 hover:text-secondaryText hover:border-black/10'
          }
        `}
      >
        Nocibé Mode
      </button>

      {isNocibe && (
        <motion.p
          initial={{ opacity: 0, x: -8 }}
          animate={{ opacity: 1, x: 0 }}
          className="font-data text-[0.55rem] text-tertiaryText uppercase tracking-widest ml-2"
        >
          Competitor topology — public data only
        </motion.p>
      )}
    </div>
  );
}
