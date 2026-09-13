import React, { useEffect, useRef, useState } from 'react';
import './HowItWorks.css';
import img12 from '../assets/12.png';
import img13 from '../assets/13.png';
import BotpressChat from './Botpresschat'; // Import the BotpressChat component

const clientId = "937df5a6-4a7e-4994-8a10-fa0916b4e18b";

export default function HowItWorks() {
  const introRef = useRef(null);
  const detailsRef = useRef(null);
  const [introVisible, setIntroVisible] = useState(false);
  const [detailsVisible, setDetailsVisible] = useState(false);
  const [num1, setNum1] = useState(0); // For 95%
  const [num2, setNum2] = useState(0); // For 1000+

  useEffect(() => {
    const observerOptions = {
      root: null, // Observe in the viewport
      threshold: 0.1, // Trigger when 10% of the section is visible
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          if (entry.target === introRef.current) {
            setIntroVisible(true);
            animateNumbers(); // Start number animation when intro section is visible
          } else if (entry.target === detailsRef.current) {
            setDetailsVisible(true);
          }
        }
      });
    }, observerOptions);

    if (introRef.current) observer.observe(introRef.current);
    if (detailsRef.current) observer.observe(detailsRef.current);

    return () => {
      if (introRef.current) observer.unobserve(introRef.current);
      if (detailsRef.current) observer.unobserve(detailsRef.current);
    };
  }, []);

  // Number animation function
  const animateNumbers = () => {
    let targetNum1 = 95;
    let targetNum2 = 1000;

    let step1 = (targetNum1 - num1) / 60; // Adjust the 60 for duration control
    let step2 = (targetNum2 - num2) / 60;

    const interval = setInterval(() => {
      setNum1((prevNum1) => {
        let newNum = prevNum1 + step1;
        if (newNum >= targetNum1) {
          newNum = targetNum1;
          clearInterval(interval);
        }
        return newNum;
      });
      setNum2((prevNum2) => {
        let newNum = prevNum2 + step2;
        if (newNum >= targetNum2) {
          newNum = targetNum2;
        }
        return newNum;
      });
    }, 36); // Approximately 60fps, 1000ms / 60 = ~16ms
  };

  // Redirect function when "Try Now" button is clicked
  const handleClick = () => {
    window.location.href = 'https://packmate-nqjjl4rmhwypmuy8tmdhid.streamlit.app/';
  };

  return (
    <div className="how-it-works-container">
      <main className="main-content">
        {/* Intro Section */}
        <section
          ref={introRef}
          className={`intro-section ${introVisible ? 'animate' : ''}`}
        >
          <div className="intro-content">
            <img src={img12} alt="AI Packing Assistant" className="intro-image" />
            <div className="text-content">
              <h2 className="section-title">Revolutionize Your Packing with AI</h2>
              <p className="section-description">
                PackMate's AI assistant simplifies your travel preparation by
                offering personalized packing suggestions.
              </p>
              <div className="stats-container">
                <div className="stat">
                  <h3 className="stat-value">{Math.round(num1)}%</h3>
                  <p className="stat-description">User approval rate</p>
                </div>
                <button className="try-now-button" onClick={handleClick}>
                  Try Now
                </button>
                <div className="stat">
                  <h3 className="stat-value">{Math.round(num2)}+</h3>
                  <p className="stat-description">Successful AI-assisted trips</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Details Section */}
        <section
          ref={detailsRef}
          className={`details-section ${detailsVisible ? 'animate' : ''}`}
        >
          <img src={img13} alt="Travel Details Input" className="details-image" />
          <div className="details-text">
            <h2 className="section-title">Effortlessly Input Your Travel Details</h2>
            <p className="section-description">
              Simply enter your destination, travel dates, and planned activities.
              Our AI analyzes the information to provide you with a personalized
              packing checklist, ensuring you have everything you need for your
              trip.
            </p>
            <ul className="details-list">
              <li>Enter your travel destination and dates</li>
              <li>Select your planned activities</li>
              <li>Receive a customized packing list</li>
            </ul>
          </div>
        </section>
      </main>
      <BotpressChat />
    </div>
  );
}
