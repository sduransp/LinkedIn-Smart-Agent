import React, { useEffect, useState } from 'react';
import mockData from './mockData.json'; // Importar mockData
import mockDataEmployees from './mockData_employess.json'; // Importar mockData_employees
import './results.css';

const Results = () => {
    const [results, setResults] = useState({});
    const [employees, setEmployees] = useState({});
    const [selectedCompany, setSelectedCompany] = useState(null);

    useEffect(() => {
        // Simular la recepción de datos
        setResults(mockData);
        setEmployees(mockDataEmployees);
        console.log('Mock data loaded:', mockData);
        console.log('Mock employees loaded:', mockDataEmployees);
    }, []);

    const handleCardClick = (company) => {
        console.log('Card clicked:', company);
        setSelectedCompany(company);
    };

    const handleClose = (e) => {
        console.log('Modal clicked:', e.target.className);
        if (e.target.classList.contains('modal') || e.target.classList.contains('close')) {
            setSelectedCompany(null);
        }
    };

    const getProcessedName = (name) => {
        const words = name.split(' ');
        return words.length > 2 ? words.slice(0, 2).join(' ') : name;
    };

    return (
        <div className="background">
            <div className="results-title">
                {Object.keys(results).length === 0 && <p>No results found.</p>}
            </div>
            <div className="results-grid">
                {Object.keys(results).map((companyName, index) => {
                    const company = results[companyName];
                    return (
                        <div key={index} className="result-card" onClick={() => handleCardClick(company)}>
                            <img src={company.image} alt={`${company.name} logo`} width="50" />
                            <h2><strong>{getProcessedName(company.name)}</strong></h2>
                            <p>Score: {company.potential_customer}</p>
                        </div>
                    );
                })}
            </div>

            {selectedCompany && (
                <div className="modal" onClick={handleClose} style={{ display: 'flex' }}>
                    <div className="modal-content">
                        <span className="close" onClick={() => setSelectedCompany(null)}>&times;</span>
                        <div style={{ position: 'relative', textAlign: 'center' }}>
                            <img src={selectedCompany.image} alt={`${selectedCompany.name} logo`} width="150" />
                            <h2>{selectedCompany.name}</h2>
                            <div style={{ position: 'absolute', top: '10px', right: '20px' }}>
                                <p><strong>Potential Customer Score:</strong> {selectedCompany.potential_customer}</p>
                            </div>
                        </div>
                        <p><strong>Founded:</strong> {selectedCompany.founded}</p>
                        <p><strong>Company Size:</strong> {selectedCompany.company_size}</p>
                        <p><strong>Industry:</strong> {selectedCompany.industry}</p>
                        <p><strong>Specialties:</strong> {selectedCompany.specialties}</p>
                        <p><strong>Description:</strong> {selectedCompany.about_us}</p>
                        <p><strong>Why is it a potential customer?</strong> {selectedCompany.reason}</p>
                        <a href={selectedCompany.linkedin_url} target="_blank" rel="noopener noreferrer">Go to the linkedin website</a>
                        <div>
                            <h2>Contacts:</h2>
                            <div className="employee-grid">
                                {employees[selectedCompany.name]?.map((employee, empIndex) => (
                                    <div key={empIndex} className="employee-card">
                                        <img src={employee.image} alt={`${employee.name} photo`} width="100" />
                                        <p><strong>{employee.name}</strong></p>
                                        <p>{employee.position}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Results;