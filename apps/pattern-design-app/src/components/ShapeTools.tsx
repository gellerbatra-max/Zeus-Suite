import { useState } from 'react'

// Gerber's "Create Piece - Rectangle" / "Create Piece - Circle": type dimensions instead of
// manually clicking every perimeter point.
interface Props {
  onRectangle: (widthMm: number, heightMm: number) => void
  onCircle: (radiusMm: number) => void
  disabled: boolean
}

export function ShapeTools({ onRectangle, onCircle, disabled }: Props) {
  const [width, setWidth] = useState('300')
  const [height, setHeight] = useState('400')
  const [radius, setRadius] = useState('150')

  return (
    <div className="shape-tools">
      <span className="shape-tools__label">New shape:</span>
      <div className="shape-tools__group">
        <input
          type="number"
          min="1"
          value={width}
          onChange={(e) => setWidth(e.target.value)}
          aria-label="Rectangle width (mm)"
        />
        <span>×</span>
        <input
          type="number"
          min="1"
          value={height}
          onChange={(e) => setHeight(e.target.value)}
          aria-label="Rectangle height (mm)"
        />
        <span className="hint">mm</span>
        <button
          disabled={disabled}
          onClick={() => onRectangle(Number(width), Number(height))}
        >
          Rectangle
        </button>
      </div>
      <div className="shape-tools__group">
        <input
          type="number"
          min="1"
          value={radius}
          onChange={(e) => setRadius(e.target.value)}
          aria-label="Circle radius (mm)"
        />
        <span className="hint">mm radius</span>
        <button disabled={disabled} onClick={() => onCircle(Number(radius))}>
          Circle
        </button>
      </div>
    </div>
  )
}
