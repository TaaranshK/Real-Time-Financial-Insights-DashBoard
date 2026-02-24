"""
DASHBOARD PAGE - Portfolio overview and stats

Shows:
- Portfolio summary
- Key metrics (gains, returns)
- Recent analyses
- Portfolio charts
- Quick actions
"""

// src/pages/Dashboard.jsx

import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { portfolioAPI, analysisAPI } from '../services/api';
import { FiTrendingUp, FiBarChart2, FiPieChart, FiArrowUpRight, FiArrowDownLeft } from 'react-icons/fi';

export default function Dashboard() {
  // -------- STATE --------
  const { user } = useAuth();
  const [portfolios, setPortfolios] = useState([]);
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedPortfolio, setSelectedPortfolio] = useState(null);

  // -------- FETCH DATA --------
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError('');

      // Fetch portfolios
      const portfoliosRes = await portfolioAPI.getPortfolios();
      const portfoliosData = portfoliosRes.data.portfolios || [];
      setPortfolios(portfoliosData);

      if (portfoliosData.length > 0) {
        setSelectedPortfolio(portfoliosData[0]);
      }

      // Fetch analyses
      const analysesRes = await analysisAPI.getAnalyses(5);
      setAnalyses(analysesRes.data.analyses || []);
    } catch (err) {
      setError('Failed to load data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // -------- LOADING STATE --------
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  // -------- RENDER --------
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome back, {user?.first_name || 'Investor'}</p>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {portfolios.length === 0 ? (
        // No Portfolio
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <FiPieChart className="mx-auto text-gray-400 mb-4" size={48} />
          <h2 className="text-xl font-semibold text-gray-800 mb-2">No Portfolios Yet</h2>
          <p className="text-gray-600 mb-4">Create your first portfolio to get started</p>
          <button className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg">
            Create Portfolio
          </button>
        </div>
      ) : (
        <>
          {/* Portfolio Summary */}
          {selectedPortfolio && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Total Invested */}
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-600 text-sm font-semibold">Total Invested</p>
                <p className="text-2xl font-bold text-gray-800 mt-2">
                  ₹{(selectedPortfolio.total_invested || 0).toLocaleString('en-IN')}
                </p>
              </div>

              {/* Current Value */}
              <div className="bg-white rounded-lg shadow p-6">
                <p className="text-gray-600 text-sm font-semibold">Current Value</p>
                <p className="text-2xl font-bold text-gray-800 mt-2">
                  ₹{(selectedPortfolio.total_current_value || 0).toLocaleString('en-IN')}
                </p>
              </div>

              {/* Total Gain/Loss */}
              <div className={`bg-white rounded-lg shadow p-6`}>
                <p className="text-gray-600 text-sm font-semibold">Total Gain/Loss</p>
                <div className="flex items-center mt-2">
                  {selectedPortfolio.total_gain_loss >= 0 ? (
                    <FiArrowUpRight className="text-green-500 mr-2" size={24} />
                  ) : (
                    <FiArrowDownLeft className="text-red-500 mr-2" size={24} />
                  )}
                  <p className={`text-2xl font-bold ${selectedPortfolio.total_gain_loss >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                    ₹{Math.abs(selectedPortfolio.total_gain_loss || 0).toLocaleString('en-IN')}
                  </p>
                </div>
              </div>

              {/* Return % */}
              <div className={`bg-white rounded-lg shadow p-6`}>
                <p className="text-gray-600 text-sm font-semibold">Return %</p>
                <p className={`text-2xl font-bold mt-2 ${selectedPortfolio.total_gain_loss_percentage >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                  {(selectedPortfolio.total_gain_loss_percentage || 0).toFixed(2)}%
                </p>
              </div>
            </div>
          )}

          {/* Recent Analyses */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-800">Recent AI Analyses</h2>
              <a href="/analysis" className="text-blue-500 hover:text-blue-700 text-sm">
                View All
              </a>
            </div>

            {analyses.length === 0 ? (
              <p className="text-gray-600 py-8 text-center">No analyses yet. Start analyzing stocks!</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="border-b border-gray-200">
                    <tr>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Stock</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Recommendation</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Sentiment</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Confidence</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Target</th>
                    </tr>
                  </thead>
                  <tbody>
                    {analyses.map((analysis) => (
                      <tr key={analysis.id} className="border-b border-gray-100 hover:bg-gray-50">
                        <td className="py-3 px-4">
                          <div>
                            <p className="font-semibold text-gray-800">{analysis.stock_symbol}</p>
                            <p className="text-sm text-gray-600">{analysis.stock_name}</p>
                          </div>
                        </td>
                        <td className="py-3 px-4">
                          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                            analysis.recommendation.includes('BUY') 
                              ? 'bg-green-100 text-green-700'
                              : analysis.recommendation === 'HOLD'
                              ? 'bg-yellow-100 text-yellow-700'
                              : 'bg-red-100 text-red-700'
                          }`}>
                            {analysis.recommendation}
                          </span>
                        </td>
                        <td className="py-3 px-4">
                          <span className={`text-sm font-semibold ${
                            analysis.sentiment === 'BULLISH'
                              ? 'text-green-600'
                              : analysis.sentiment === 'NEUTRAL'
                              ? 'text-yellow-600'
                              : 'text-red-600'
                          }`}>
                            {analysis.sentiment}
                          </span>
                        </td>
                        <td className="py-3 px-4">
                          <div className="w-16 bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-500 h-2 rounded-full"
                              style={{ width: `${analysis.confidence_score}%` }}
                            ></div>
                          </div>
                          <p className="text-sm text-gray-600 mt-1">{analysis.confidence_score.toFixed(0)}%</p>
                        </td>
                        <td className="py-3 px-4">
                          <p className="font-semibold text-gray-800">₹{analysis.price_target || 'N/A'}</p>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg flex items-center justify-center font-semibold transition">
              <FiTrendingUp className="mr-2" size={20} />
              Analyze Stocks
            </button>
            <button className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg flex items-center justify-center font-semibold transition">
              <FiBarChart2 className="mr-2" size={20} />
              Add to Portfolio
            </button>
            <button className="bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-lg flex items-center justify-center font-semibold transition">
              <FiPieChart className="mr-2" size={20} />
              Portfolio Report
            </button>
          </div>
        </>
      )}
    </div>
  );
}
