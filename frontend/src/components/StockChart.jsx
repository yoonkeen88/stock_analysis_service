import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import { useState } from 'react';
import './StockChart.css';

/**
 * 주식 시세 차트 컴포넌트
 * Recharts를 사용한 반응형 차트
 */
const StockChart = ({ data = [], symbol = '' }) => {
  const [hoveredData, setHoveredData] = useState(null);

  // 데이터 포맷팅 (Recharts 형식으로 변환)
  const chartData = data.map((item) => ({
    date: new Date(item.date).toLocaleDateString('ko-KR', { 
      month: 'short', 
      day: 'numeric' 
    }),
    fullDate: new Date(item.date).toLocaleDateString('ko-KR'),
    open: parseFloat(item.open),
    high: parseFloat(item.high),
    low: parseFloat(item.low),
    close: parseFloat(item.close),
    volume: parseInt(item.volume),
  }));

  // 커스텀 툴팁 컴포넌트
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="chart-tooltip">
          <div className="tooltip-header">
            <strong>{data.fullDate}</strong>
          </div>
          <div className="tooltip-content">
            <div className="tooltip-item">
              <span className="tooltip-label">시가:</span>
              <span className="tooltip-value open">${data.open.toFixed(2)}</span>
            </div>
            <div className="tooltip-item">
              <span className="tooltip-label">고가:</span>
              <span className="tooltip-value high">${data.high.toFixed(2)}</span>
            </div>
            <div className="tooltip-item">
              <span className="tooltip-label">저가:</span>
              <span className="tooltip-value low">${data.low.toFixed(2)}</span>
            </div>
            <div className="tooltip-item">
              <span className="tooltip-label">종가:</span>
              <span className="tooltip-value close">${data.close.toFixed(2)}</span>
            </div>
            <div className="tooltip-item">
              <span className="tooltip-label">거래량:</span>
              <span className="tooltip-value volume">
                {data.volume.toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      );
    }
    return null;
  };

  if (!chartData || chartData.length === 0) {
    return (
      <div className="chart-empty">
        <p>차트 데이터가 없습니다.</p>
      </div>
    );
  }

  // 최신 종가 (현재 가격으로 표시)
  const currentPrice = chartData[chartData.length - 1]?.close || 0;
  const firstPrice = chartData[0]?.close || 0;
  const priceChange = currentPrice - firstPrice;
  const priceChangePercent = ((priceChange / firstPrice) * 100).toFixed(2);

  return (
    <div className="stock-chart">
      <div className="chart-header">
        <div className="chart-title">
          <h3>{symbol} 시세 차트</h3>
          <div className="chart-price-info">
            <span className="current-price">${currentPrice.toFixed(2)}</span>
            <span className={`price-change ${priceChange >= 0 ? 'positive' : 'negative'}`}>
              {priceChange >= 0 ? '+' : ''}
              {priceChange.toFixed(2)} ({priceChangePercent}%)
            </span>
          </div>
        </div>
      </div>
      
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={400}>
          <LineChart
            data={chartData}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            onMouseMove={(e) => {
              if (e && e.activePayload) {
                setHoveredData(e.activePayload[0].payload);
              }
            }}
            onMouseLeave={() => setHoveredData(null)}
          >
            <CartesianGrid 
              strokeDasharray="3 3" 
              stroke="var(--border-default)"
              opacity={0.3}
            />
            <XAxis 
              dataKey="date" 
              stroke="var(--text-tertiary)"
              style={{ fontSize: '12px' }}
            />
            <YAxis 
              stroke="var(--text-tertiary)"
              style={{ fontSize: '12px' }}
              domain={['dataMin - 5', 'dataMax + 5']}
            />
            <Tooltip content={<CustomTooltip />} />
            <ReferenceLine 
              y={currentPrice} 
              stroke="var(--color-primary)" 
              strokeDasharray="2 2"
              opacity={0.5}
            />
            <Line
              type="monotone"
              dataKey="close"
              stroke="var(--color-primary)"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 6, fill: 'var(--color-primary)' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* 호버 시 상세 정보 표시 */}
      {hoveredData && (
        <div className="chart-hover-info">
          <div className="hover-info-card">
            <div className="hover-date">{hoveredData.fullDate}</div>
            <div className="hover-prices">
              <div className="price-row">
                <span>시가</span>
                <span className="price-value">${hoveredData.open.toFixed(2)}</span>
              </div>
              <div className="price-row">
                <span>고가</span>
                <span className="price-value high">${hoveredData.high.toFixed(2)}</span>
              </div>
              <div className="price-row">
                <span>저가</span>
                <span className="price-value low">${hoveredData.low.toFixed(2)}</span>
              </div>
              <div className="price-row">
                <span>종가</span>
                <span className="price-value close">${hoveredData.close.toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StockChart;

