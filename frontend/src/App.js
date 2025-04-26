import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './components/HomePage';
import AnimalInfoForm from './components/AnimalInfoForm';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/animal-info" element={<AnimalInfoForm />} />


          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;