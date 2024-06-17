import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './results.css';

const Results = () => {
    const location = useLocation();
    const { results: initialResults, employees: initialEmployees } = location.state || { results: {}, employees: {} };

    const [results, setResults] = useState(initialResults);
    const [employees, setEmployees] = useState(initialEmployees);
    const [selectedCompany, setSelectedCompany] = useState(null);
    const [selectedEmployee, setSelectedEmployee] = useState(null);

    useEffect(() => {
        setResults(initialResults);
        setEmployees(initialEmployees);
        console.log('Results loaded:', initialResults);
        console.log('Employees loaded:', initialEmployees);
    }, [initialResults, initialEmployees]);

    const handleCardClick = (company) => {
        console.log('Card clicked:', company);
        setSelectedCompany(company);
    };

    const handleEmployeeClick = (employee) => {
        console.log('Employee clicked:', employee);
        setSelectedEmployee(employee);
    };

    const handleClose = (e) => {
        console.log('Modal clicked:', e.target.className);
        if (e.target.classList.contains('modal') || e.target.classList.contains('close')) {
            setSelectedCompany(null);
            setSelectedEmployee(null);
        }
    };

    const getProcessedName = (name) => {
        const words = name.split(' ');
        return words.length > 2 ? words.slice(0, 2).join(' ') : name;
    };

    return (
        <div className="background">
            <div className="results-title">
                {Object.keys(results).length === 0 && <p style={{ fontSize: '36px' }}>No results found.</p>}
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
                        <div style={{ textAlign: 'center' }}>
                            <a 
                                href={selectedCompany.linkedin_url} 
                                target="_blank" 
                                rel="noopener noreferrer" 
                                className="linkedin-button"
                            >
                                LinkedIn Website
                            </a>
                        </div>
                        <div>
                            <h2>Contacts:</h2>
                            <div className="employee-grid">
                                {employees[selectedCompany.name]?.map((employee, empIndex) => (
                                    <div key={empIndex} className="employee-card" onClick={() => handleEmployeeClick(employee)}>
                                        <img src={employee.image} alt={`${employee.name} photo`} width="100" />
                                        <p><strong>{employee.name}</strong></p>
                                        <p>{employee.position}</p>
                                        <p><strong>Compatibility Score:</strong> {employee.contact_of_interest}</p>
                                    </div>
                                ))}
                            </div>
                            <button className="send-message-button">Contact All</button>
                        </div>
                    </div>
                </div>
            )}

            {selectedEmployee && (
                <div className="modal" onClick={handleClose} style={{ display: 'flex' }}>
                    <div className="modal-content">
                        <span className="close" onClick={() => setSelectedEmployee(null)}>&times;</span>
                        <div className="employee-details">
                            <div className="employee-details-left" style={{ textAlign: 'left' }}>
                                <img src={selectedEmployee.image} alt={`${selectedEmployee.name} photo`} width="150" />
                                <h2>{selectedEmployee.name}</h2>
                                <p><strong>Position:</strong> {selectedEmployee.position}</p>
                                <p><strong>Location:</strong> {selectedEmployee.location}</p>
                                <p><strong>Compatibility Score:</strong> {selectedEmployee.contact_of_interest}</p>
                            </div>
                            <div className="employee-details-right">
                                <h3>Education:</h3>
                                <ul>
                                    {selectedEmployee.educations.map((education, index) => (
                                        <li key={index}>
                                            <p><strong>Institution:</strong> {education.institution_name}</p>
                                            <p><strong>Degree:</strong> {education.degree}</p>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                        <p><strong>Reason:</strong> {selectedEmployee.reason}</p>
                        <button className="send-message-button">Send Message</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Results;

// import React, { useEffect, useState } from 'react';
// import mockData from './mockData.json'; // Importar mockData
// import mockDataEmployees from './mockData_employess.json'; // Importar mockData_employees
// import './results.css';

// const Results = () => {
//     const [results, setResults] = useState({});
//     const [employees, setEmployees] = useState({});
//     const [selectedCompany, setSelectedCompany] = useState(null);
//     const [selectedEmployee, setSelectedEmployee] = useState(null);

//     useEffect(() => {
//         // Simular la recepción de datos
//         setResults(mockData);
//         setEmployees(mockDataEmployees);
//         console.log('Mock data loaded:', mockData);
//         console.log('Mock employees loaded:', mockDataEmployees);
//     }, []);

//     const handleCardClick = (company) => {
//         console.log('Card clicked:', company);
//         setSelectedCompany(company);
//     };

//     const handleEmployeeClick = (employee) => {
//         console.log('Employee clicked:', employee);
//         setSelectedEmployee(employee);
//     };

//     const handleClose = (e) => {
//         console.log('Modal clicked:', e.target.className);
//         if (e.target.classList.contains('modal') || e.target.classList.contains('close')) {
//             setSelectedCompany(null);
//             setSelectedEmployee(null);
//         }
//     };

//     const getProcessedName = (name) => {
//         const words = name.split(' ');
//         return words.length > 2 ? words.slice(0, 2).join(' ') : name;
//     };

//     return (
//         <div className="background">
//             <div className="results-title">
//                 {Object.keys(results).length === 0 && <p>No results found.</p>}
//             </div>
//             <div className="results-grid">
//                 {Object.keys(results).map((companyName, index) => {
//                     const company = results[companyName];
//                     return (
//                         <div key={index} className="result-card" onClick={() => handleCardClick(company)}>
//                             <img src={company.image} alt={`${company.name} logo`} width="50" />
//                             <h2><strong>{getProcessedName(company.name)}</strong></h2>
//                             <p>Score: {company.potential_customer}</p>
//                         </div>
//                     );
//                 })}
//             </div>

//             {selectedCompany && (
//                 <div className="modal" onClick={handleClose} style={{ display: 'flex' }}>
//                     <div className="modal-content">
//                         <span className="close" onClick={() => setSelectedCompany(null)}>&times;</span>
//                         <div style={{ position: 'relative', textAlign: 'center' }}>
//                             <img src={selectedCompany.image} alt={`${selectedCompany.name} logo`} width="150" />
//                             <h2>{selectedCompany.name}</h2>
//                             <div style={{ position: 'absolute', top: '10px', right: '20px' }}>
//                                 <p><strong>Potential Customer Score:</strong> {selectedCompany.potential_customer}</p>
//                             </div>
//                         </div>
//                         <p><strong>Founded:</strong> {selectedCompany.founded}</p>
//                         <p><strong>Company Size:</strong> {selectedCompany.company_size}</p>
//                         <p><strong>Industry:</strong> {selectedCompany.industry}</p>
//                         <p><strong>Specialties:</strong> {selectedCompany.specialties}</p>
//                         <p><strong>Description:</strong> {selectedCompany.about_us}</p>
//                         <p><strong>Why is it a potential customer?</strong> {selectedCompany.reason}</p>
//                         <div style={{ textAlign: 'center' }}>
//                             <a href={selectedCompany.linkedin_url} target="_blank" rel="noopener noreferrer">Go to the linkedin website</a>
//                         </div>
//                         <div>
//                             <h2>Contacts:</h2>
//                             <div className="employee-grid">
//                                 {employees[selectedCompany.name]?.map((employee, empIndex) => (
//                                     <div key={empIndex} className="employee-card" onClick={() => handleEmployeeClick(employee)}>
//                                         <img src={employee.image} alt={`${employee.name} photo`} width="100" />
//                                         <p><strong>{employee.name}</strong></p>
//                                         <p>{employee.position}</p>
//                                         <p><strong>Score:</strong> {employee.contact_of_interest}</p>
//                                     </div>
//                                 ))}
//                             </div>
//                             <button className="send-message-button">Contact All</button>
//                         </div>
//                     </div>
//                 </div>
//             )}

//             {selectedEmployee && (
//                 <div className="modal" onClick={handleClose} style={{ display: 'flex' }}>
//                     <div className="modal-content">
//                         <span className="close" onClick={() => setSelectedEmployee(null)}>&times;</span>
//                         <div className="employee-details">
//                             <div className="employee-details-left" style={{ textAlign: 'left' }}>
//                                 <img src={selectedEmployee.image} alt={`${selectedEmployee.name} photo`} width="150" />
//                                 <h2>{selectedEmployee.name}</h2>
//                                 <p><strong>Position:</strong> {selectedEmployee.position}</p>
//                                 <p><strong>Location:</strong> {selectedEmployee.location}</p>
//                                 <p><strong>Compatibility Score:</strong> {selectedEmployee.contact_of_interest}</p>
//                             </div>
//                             <div className="employee-details-right">
//                                 <h3>Education:</h3>
//                                 <ul>
//                                     {selectedEmployee.educations.map((education, index) => (
//                                         <li key={index}>
//                                             <p><strong>Institution:</strong> {education.institution_name}</p>
//                                             <p><strong>Degree:</strong> {education.degree}</p>
//                                         </li>
//                                     ))}
//                                 </ul>
//                             </div>
//                         </div>
//                         <p><strong>Reason:</strong> {selectedEmployee.reason}</p>
//                         <button className="send-message-button">Send Message</button>
//                     </div>
//                 </div>
//             )}
//         </div>
//     );
// };

// export default Results;