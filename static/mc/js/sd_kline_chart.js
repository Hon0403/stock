document.addEventListener('DOMContentLoaded', function() {
    const btnKline = document.getElementById('btn-kline');
    const dateRangeOptions = document.getElementById('date-range-options');
    const updateChartBtn = document.getElementById('update-chart');

    btnKline.addEventListener('click', function() {
        dateRangeOptions.style.display = 'block';
    });

    updateChartBtn.addEventListener('click', function() {
        const selectedRanges = Array.from(document.querySelectorAll('input[name="date_range"]:checked'))
            .map(checkbox => checkbox.value);
        fetchKLineData(selectedRanges);
    });

    function fetchKLineData(ranges) {
        fetch(`/stock_data?k_line_ranges=${ranges.join(',')}`)
            .then(response => response.json())
            .then(data => {
                displayKLineChart(data);
            })
            .catch(error => console.error('Error fetching K-line data:', error));
    }

    function displayKLineChart(data) {
        const svg = d3.select('#kline-chart');
        svg.selectAll('*').remove(); // Clear existing content

        data.forEach(rangeData => {
            const width = svg.node().getBoundingClientRect().width;
            const height = svg.node().getBoundingClientRect().height;
            const margin = { top: 20, right: 20, bottom: 30, left: 50 };
            
            const x = d3.scaleTime().range([0, width - margin.left - margin.right]);
            const y = d3.scaleLinear().range([height - margin.top - margin.bottom, 0]);

            const kLineData = rangeData.data;
            x.domain(d3.extent(kLineData, d => new Date(d.date)));
            y.domain([d3.min(kLineData, d => d.low), d3.max(kLineData, d => d.high)]);

            const xAxis = d3.axisBottom(x);
            const yAxis = d3.axisLeft(y);

            svg.append('g')
                .attr('class', 'x axis')
                .attr('transform', `translate(${margin.left},${height - margin.bottom})`)
                .call(xAxis);

            svg.append('g')
                .attr('class', 'y axis')
                .attr('transform', `translate(${margin.left},${margin.top})`)
                .call(yAxis);

            svg.selectAll('.candle')
                .data(kLineData)
                .enter().append('rect')
                .attr('class', 'candle')
                .attr('x', d => x(new Date(d.date)) - 5)
                .attr('y', d => y(Math.max(d.open, d.close)))
                .attr('width', 10)
                .attr('height', d => Math.abs(y(d.open) - y(d.close)))
                .attr('fill', d => d.open > d.close ? 'red' : 'green')
                .attr('transform', `translate(${margin.left},${margin.top})`);

            svg.selectAll('.stem')
                .data(kLineData)
                .enter().append('line')
                .attr('class', 'stem')
                .attr('x1', d => x(new Date(d.date)))
                .attr('x2', d => x(new Date(d.date)))
                .attr('y1', d => y(d.high))
                .attr('y2', d => y(d.low))
                .attr('stroke', 'black')
                .attr('transform', `translate(${margin.left},${margin.top})`);

            svg.append('text')
                .attr('x', width / 2)
                .attr('y', margin.top)
                .attr('text-anchor', 'middle')
                .text(`K線圖 (${rangeData.range})`);
        });
    }
});
