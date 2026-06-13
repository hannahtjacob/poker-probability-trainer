declare module 'react-plotly.js' {
  import type { CSSProperties, ComponentType } from 'react'
  import type { Config, Data, Layout } from 'plotly.js'

  interface PlotProps {
    data: Data[]
    layout?: Partial<Layout>
    config?: Partial<Config>
    className?: string
    style?: CSSProperties
    useResizeHandler?: boolean
  }

  const Plot: ComponentType<PlotProps>

  export default Plot
}
