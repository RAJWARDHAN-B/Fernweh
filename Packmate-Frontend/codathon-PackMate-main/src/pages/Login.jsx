import React, { useState } from 'react';
import './Login.css';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSignup = (e) => {
    e.preventDefault();
    
    if (password === confirmPassword) {
      // Prepare the user data in JSON format
      const userData = {
        email: email,
        password: password
      };

      // Log the user data in JSON format
      console.log(JSON.stringify(userData));

      // Reset form fields
      setEmail('');
      setPassword('');
      setConfirmPassword('');
    } else {
      console.log('Passwords do not match');
    }
  };

  return (
    <div className="login-page-wrap">
    <div className="signup-container">
      <h2>Create Your Account</h2>
      <form onSubmit={handleSignup} className="signup-form">
        <label htmlFor="signup-email">Email</label>
        <input 
          type="email" 
          id="signup-email"  // Unique ID for signup email
          placeholder="Enter your email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
        />

        <label htmlFor="signup-password">Password</label>
        <input 
          type="password" 
          id="signup-password"  // Unique ID for signup password
          placeholder="Enter your password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
        />

        <label htmlFor="signup-confirm-password">Confirm Password</label>
        <input 
          type="password" 
          id="signup-confirm-password"  // Unique ID for confirm password
          placeholder="Confirm your password" 
          value={confirmPassword} 
          onChange={(e) => setConfirmPassword(e.target.value)} 
        />

        <button type="submit" className="signup-btn">Sign Up</button>
      </form>

      <footer className="footer-signup">
        <p>Already have an account? <a href="/login">Login</a></p>
      </footer>
    </div>
    </div>
  );
}
