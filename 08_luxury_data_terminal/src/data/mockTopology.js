// Data strictly structured from the Sephora Luxury Data Terminal dataset

export const categories = {
  SKINCARE: 'Skincare',
  MAKEUP: 'Make up',
  FRAGRANCE: 'Fragrance',
  HAIRCARE: 'Haircare',
};

// 20 Nodes to maintain 60fps physics fluidity
export const nodes = [
  { id: 'DRUNK ELEPHANT', group: categories.SKINCARE },
  { id: 'FRESH SAS', group: categories.SKINCARE },
  { id: 'KIEHLS', group: categories.SKINCARE },
  { id: 'LANCOME', group: categories.FRAGRANCE },
  { id: 'LAUDER', group: categories.SKINCARE },
  { id: 'DIOR', group: categories.FRAGRANCE },
  { id: 'SISLEY', group: categories.FRAGRANCE },
  { id: 'ARMANI', group: categories.FRAGRANCE },
  { id: 'GLOSSIER', group: categories.MAKEUP },
  { id: 'KERASTASE', group: categories.HAIRCARE },
  { id: 'LEONOR GREYL', group: categories.HAIRCARE },
  { id: 'AVEDA', group: categories.HAIRCARE },
  { id: 'GUERLAIN', group: categories.FRAGRANCE },
  { id: 'CHAMPO', group: categories.HAIRCARE },
  { id: 'CHARLOTTE TILBURY', group: categories.MAKEUP },
  { id: 'COLOR WOW', group: categories.MAKEUP },
  { id: 'BENEFIT', group: categories.MAKEUP },
  { id: 'BENEFIT SERVICE', group: categories.MAKEUP },
  { id: 'NARS', group: categories.MAKEUP },
  { id: 'OLAPLEX', group: categories.HAIRCARE },
];

export const links = [
  { source: 'DRUNK ELEPHANT', target: 'FRESH SAS', lift: 11.73, isAffinity: true },
  { source: 'KIEHLS', target: 'LANCOME', lift: 2.16, isAffinity: true },
  { source: 'KIEHLS', target: 'LAUDER', lift: 1.96, isAffinity: true },
  { source: 'DIOR', target: 'SISLEY', lift: 1.63, isAffinity: true },
  { source: 'ARMANI', target: 'KIEHLS', lift: 1.61, isAffinity: true },
  { source: 'GLOSSIER', target: 'KERASTASE', lift: 2.62, isAffinity: true },
  { source: 'LANCOME', target: 'LEONOR GREYL', lift: 2.86, isAffinity: true },
  { source: 'AVEDA', target: 'GUERLAIN', lift: 1.91, isAffinity: true },
  { source: 'CHAMPO', target: 'DIOR', lift: 4.96, isAffinity: true },
  { source: 'CHARLOTTE TILBURY', target: 'COLOR WOW', lift: 1.71, isAffinity: true },
  { source: 'BENEFIT', target: 'BENEFIT SERVICE', lift: 3.93, isAffinity: true },
];

// For the standard graph visualization (Standard Market logic)
// Nodes will cluster by their own `group` (Category).
// Real connections are not drawn during standard clustering,
// only the physical categories matter to show isolated bubbles.
