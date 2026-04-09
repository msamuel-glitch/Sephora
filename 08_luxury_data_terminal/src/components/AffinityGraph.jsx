import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { motion, AnimatePresence } from 'framer-motion';
import { nodes, links } from '../data/mockTopology';
import { NOCIBE_FINDING } from '../data/validatedData';

const CATEGORY_COLORS = {
  'Skincare':  '#8BB6A0',
  'Make up':   '#C9847C',
  'Fragrance': '#B8A89A',
  'Haircare':  '#7B9EBF',
};

export default function AffinityGraph({ isNocibe }) {
  const svgRef = useRef(null);
  const simRef = useRef(null);

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const width = svgRef.current?.parentElement?.clientWidth || 700;
    const height = svgRef.current?.parentElement?.clientHeight || 500;

    svg.attr('viewBox', `0 0 ${width} ${height}`);
    svg.selectAll('*').remove();

    const defs = svg.append('defs');

    // Glow filter for Sephora mode links
    const filter = defs.append('filter').attr('id', 'glow');
    filter.append('feGaussianBlur').attr('stdDeviation', '3').attr('result', 'coloredBlur');
    const feMerge = filter.append('feMerge');
    feMerge.append('feMergeNode').attr('in', 'coloredBlur');
    feMerge.append('feMergeNode').attr('in', 'SourceGraphic');

    // Deep clone nodes/links for each simulation instance
    const simNodes = nodes.map(d => ({ ...d }));
    const simLinks = isNocibe ? [] : links.map(d => ({ ...d }));

    const simulation = d3.forceSimulation(simNodes)
      .force('charge', d3.forceManyBody().strength(isNocibe ? -200 : -250))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(isNocibe ? 45 : 35))
      .force('x', d3.forceX(width / 2).strength(0.04))
      .force('y', d3.forceY(height / 2).strength(0.04));

    if (!isNocibe) {
      simulation.force('link', d3.forceLink(simLinks).id(d => d.id).distance(140).strength(0.3));
    } else {
      // In Nocibé mode, cluster by category — push nodes into wider quadrants
      const categoryPositions = {
        'Skincare':  { x: width * 0.2, y: height * 0.2 },
        'Make up':   { x: width * 0.8, y: height * 0.2 },
        'Fragrance': { x: width * 0.2, y: height * 0.8 },
        'Haircare':  { x: width * 0.8, y: height * 0.8 },
      };
      simulation
        .force('x', d3.forceX(d => categoryPositions[d.group]?.x || width / 2).strength(0.5))
        .force('y', d3.forceY(d => categoryPositions[d.group]?.y || height / 2).strength(0.5));
    }

    simRef.current = simulation;

    // Links (Sephora mode only)
    const linkGroup = svg.append('g');
    const linkElements = linkGroup.selectAll('line')
      .data(simLinks)
      .join('line')
      .attr('stroke', '#D4AF37')
      .attr('stroke-opacity', d => Math.min(d.lift / 15, 0.6))
      .attr('stroke-width', d => Math.max(1, Math.min(d.lift / 3, 4)));

    // Nodes
    const nodeGroup = svg.append('g');
    const nodeElements = nodeGroup.selectAll('g')
      .data(simNodes)
      .join('g')
      .style('cursor', 'pointer');

    // Node circles
    nodeElements.append('circle')
      .attr('r', 16)
      .attr('fill', d => CATEGORY_COLORS[d.group] || '#B8A89A')
      .attr('fill-opacity', isNocibe ? 0.3 : 0.85)
      .attr('stroke', d => isNocibe ? 'rgba(0,0,0,0.08)' : CATEGORY_COLORS[d.group])
      .attr('stroke-width', isNocibe ? 1 : 2)
      .attr('stroke-opacity', isNocibe ? 0.4 : 0.8)
      .attr('class', 'shadow-lift transition-all duration-300');

    // Node labels
    nodeElements.append('text')
      .text(d => d.id)
      .attr('dy', -22)
      .attr('text-anchor', 'middle')
      .attr('font-family', '"Inter", sans-serif')
      .attr('font-size', '10px')
      .attr('font-weight', '600')
      .attr('fill', isNocibe ? 'rgba(0,0,0,0.3)' : 'rgba(0,0,0,0.7)')
      .attr('letter-spacing', '0.02em');

    // Hover tooltip for links (Sephora mode)
    if (!isNocibe) {
      const tooltip = d3.select(svgRef.current.parentElement)
        .append('div')
        .attr('class', 'glass-tooltip')
        .style('position', 'absolute')
        .style('pointer-events', 'none')
        .style('opacity', 0)
        .style('font-size', '0.6rem')
        .style('z-index', 100);

      nodeElements
        .on('mouseenter', (event, d) => {
          // Find connected links
          const connected = simLinks.filter(l =>
            (l.source.id || l.source) === d.id || (l.target.id || l.target) === d.id
          );
          if (connected.length > 0) {
            const html = connected.map(l => {
              const partner = (l.source.id || l.source) === d.id
                ? (l.target.id || l.target)
                : (l.source.id || l.source);
              return `<div style="margin-bottom:4px"><span style="color:#D4AF37;font-weight:bold">${d.id}</span> → ${partner}: <span style="color:#D4AF37">${l.lift}×</span></div>`;
            }).join('');
            tooltip.html(html)
              .style('opacity', 1)
              .style('left', `${event.offsetX + 15}px`)
              .style('top', `${event.offsetY - 10}px`);
          }
        })
        .on('mouseleave', () => {
          tooltip.style('opacity', 0);
        });
    }

    // Category labels in Nocibé mode
    if (isNocibe) {
      const categoryPositions = {
        'Skincare':  { x: width * 0.2, y: height * 0.1 },
        'Make up':   { x: width * 0.8, y: height * 0.1 },
        'Fragrance': { x: width * 0.2, y: height * 0.9 },
        'Haircare':  { x: width * 0.8, y: height * 0.9 },
      };
      Object.entries(categoryPositions).forEach(([cat, pos]) => {
        svg.append('text')
          .attr('x', pos.x)
          .attr('y', pos.y)
          .attr('text-anchor', 'middle')
          .attr('font-family', '"Inter", sans-serif')
          .attr('font-size', '13px')
          .attr('font-weight', '700')
          .attr('letter-spacing', '0.15em')
          .attr('fill', 'rgba(0,0,0,0.25)')
          .text(cat.toUpperCase());
      });
    }

    // Tick
    simulation.on('tick', () => {
      linkElements
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      nodeElements.attr('transform', d => `translate(${d.x},${d.y})`);
    });

    return () => {
      simulation.stop();
      d3.select(svgRef.current?.parentElement).selectAll('.glass-tooltip').remove();
    };
  }, [isNocibe]);

  return (
    <div className="glass-panel h-full relative overflow-hidden" style={{ minHeight: '450px' }}>
      {/* Legend */}
      <div className="absolute top-4 left-4 z-10 flex flex-wrap gap-3">
        {Object.entries(CATEGORY_COLORS).map(([cat, color]) => (
          <div key={cat} className="flex items-center gap-1.5">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: color, opacity: isNocibe ? 0.3 : 0.8 }} />
            <span className="font-data text-[0.55rem] text-secondaryText uppercase tracking-widest">{cat}</span>
          </div>
        ))}
      </div>

      {/* SVG Canvas */}
      <svg ref={svgRef} className="w-full h-full" preserveAspectRatio="xMidYMid meet" />

      {/* Nocibé Disclosure */}
      <AnimatePresence>
        {isNocibe && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            transition={{ duration: 0.4 }}
            className="absolute bottom-4 left-4 right-4 bg-white shadow-lift border border-black/5 rounded-xl p-4 z-20"
          >
            <p className="font-data text-[0.6rem] text-secondaryText uppercase tracking-widest leading-relaxed">
              {NOCIBE_FINDING.qualitative}
            </p>
            <p className="font-data text-[0.5rem] text-tertiaryText uppercase tracking-widest mt-2 italic">
              {NOCIBE_FINDING.methodology}
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
