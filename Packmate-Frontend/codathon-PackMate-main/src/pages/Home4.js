import React, { useEffect, useState, useRef } from 'react';
import './Home4.css'; // Import the CSS file
import imgch1 from '../assets/ch1.png'; // Import the image
import imgch2 from '../assets/ch2.png'; // Import the image
import imgch3 from '../assets/ch3.png'; // Import the image

const Home4 = () => {
  const [visibleSections, setVisibleSections] = useState([]);
  const sectionsRef = useRef([]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const index = sectionsRef.current.indexOf(entry.target);
            setVisibleSections((prev) => {
              if (!prev.includes(index)) {
                return [...prev, index];
              }
              return prev;
            });
          }
        });
      },
      { threshold: 0.2 } // Trigger when 20% of the section is visible
    );

    sectionsRef.current.forEach((section) => {
      if (section) observer.observe(section);
    });

    return () => {
      sectionsRef.current.forEach((section) => {
        if (section) observer.unobserve(section);
      });
    };
  }, []);

  return (
    <div>
      {/* Testimonials Section */}
      <div className="testimonials">
        <h2>What Users Say !?</h2>
        <p>
          Discover how PackMate has transformed travel experiences for our users.
        </p>

        <div className="testimonialCards">
          {[
            {
              name: 'Emily',
              title: 'Investor',
              testimonial:
                'PackMate has completely changed the way I prepare for trips! I never forget essentials anymore, and the suggestions are spot on for my travel plans.',
              img: imgch1,
            },
            {
              name: 'Ace',
              title: 'Banker',
              testimonial:
                'Using PackMate made my last vacation stress-free! The AI recommendations were tailored perfectly to my itinerary and the weather.',
              img: imgch2,
            },
            {
              name: 'Ely',
              title: 'Traveler',
              testimonial:
                'PackMate is a game changer! I love how it adapts to my travel style and makes packing so much easier.',
              img: imgch3,
            },
          ].map((user, index) => (
            <div
              key={index}
              ref={(el) => (sectionsRef.current[index] = el)}
              className={`testimonialCard ${
                visibleSections.includes(index) ? 'visible' : ''
              }`}
            >
              <img src={user.img} alt={user.name} />
              <h3>{user.name}</h3>
              <p>{user.title}</p>
              <p className="italic">"{user.testimonial}"</p>
            </div>
          ))}
        </div>
      </div>

      {/* Footer Section */}
      <footer>
        <div className="footerContent">
          
          <div className="subscribe">
            <h2>Stay Updated</h2>
            <p>
              Subscribe to our newsletter for the latest travel tips and
              updates from PackMate.
            </p>
            <div>
              <input type="email" placeholder="Enter your email" />
              <button>Submit</button>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home4;