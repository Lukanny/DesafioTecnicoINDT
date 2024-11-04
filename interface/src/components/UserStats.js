import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import api from '../services/api';

const UserStats = () => {
  const d3Container = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/users/stats');
        renderChart(response.data);
      } catch (error) {
        alert('Erro ao buscar dados para os gráficos');
      }
    };

    const renderChart = (data) => {
      const svg = d3.select(d3Container.current);
      svg.selectAll('*').remove();

      const width = 500;
      const height = 300;

      svg.attr('width', width)
         .attr('height', height);

      const margin = { top: 20, right: 30, bottom: 40, left: 40 };
      const x = d3.scaleBand()
                  .domain(data.map(d => `${d.access_level}-${d.status}`))
                  .range([margin.left, width - margin.right])
                  .padding(0.1);
      
      const y = d3.scaleLinear()
                  .domain([0, d3.max(data, d => d.count)]).nice()
                  .range([height - margin.bottom, margin.top]);

      svg.append("g")
         .attr("fill", "steelblue")
         .selectAll("rect")
         .data(data)
         .enter().append("rect")
         .attr("x", d => x(`${d.access_level}-${d.status}`))
         .attr("y", d => y(d.count))
         .attr("height", d => y(0) - y(d.count))
         .attr("width", x.bandwidth());

      svg.append("g")
         .attr("transform", `translate(0,${height - margin.bottom})`)
         .call(d3.axisBottom(x))
         .selectAll("text")
         .attr("transform", "rotate(-45)")
         .style("text-anchor", "end");

      svg.append("g")
         .attr("transform", `translate(${margin.left},0)`)
         .call(d3.axisLeft(y));
    };

    fetchData();
  }, []);

  return (
    <div>
      <h3>Estatísticas de Usuários</h3>
      <svg ref={d3Container}></svg>
    </div>
  );
};

export default UserStats;
