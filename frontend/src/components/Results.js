import React from 'react';
import { useLocation } from 'react-router-dom';

const Results = () => {
    const location = useLocation();
    const { results } = location.state || { results: {} };

    return (
        <div>
            <h1>Search Results</h1>
            {Object.keys(results).map((companyName, index) => (
                <div key={index} className="result-card">
                    <h2>{companyName}</h2>
                    <p><strong>About Us:</strong> {results[companyName].about_us}</p>
                    <p><strong>Founded:</strong> {results[companyName].founded}</p>
                    <p><strong>Industry:</strong> {results[companyName].industry}</p>
                    <p><strong>Company Size:</strong> {results[companyName].company_size}</p>
                    <p><strong>Specialties:</strong> {results[companyName].specialties}</p>
                    <img src={results[companyName].image} alt={`${companyName} logo`} width="200" />
                </div>
            ))}
        </div>
    );
};

export default Results;