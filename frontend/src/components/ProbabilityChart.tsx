import Plot from 'react-plotly.js'


interface ProbabilityChartProps {
  winProbability: number
  tieProbability: number
  lossProbability: number
}

function ProbabilityChart({
  winProbability,
  tieProbability,
  lossProbability,
}: ProbabilityChartProps) {
  return (
    <div className="probability-chart">
      <Plot
        data={[
          {
            type: 'bar',
            x: ['Win', 'Tie', 'Loss'],
            y: [winProbability, tieProbability, lossProbability],
            marker: {
              color: ['#2e8b57', '#d4a017', '#c94c4c'],
            },
          },
        ]}
        layout={{
          title: { text: 'Outcome Probabilities' },
          autosize: true,
          margin: { t: 60, r: 20, b: 50, l: 55 },
          yaxis: {
            title: { text: 'Probability (%)' },
            range: [0, 100],
          },
        }}
        config={{
          displayModeBar: false,
          responsive: true,
        }}
        useResizeHandler
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  )
}

export default ProbabilityChart
