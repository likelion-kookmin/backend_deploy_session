// src/RegisterForm.jsx
import React, { useState } from 'react';
import axios from 'axios';

function RegisterForm() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    try {
      const response = await axios.post('http://localhost:8000/api/users/', formData); // ✅ 백엔드 주소로 변경
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data || '등록 실패');
    }
  };

  return (
    <div>
      <h2>회원가입</h2>
      <form onSubmit={handleSubmit}>
        <input name="username" placeholder="Username" onChange={handleChange} />
        <input name="email" placeholder="Email" onChange={handleChange} type="email" />
        <input name="password" placeholder="Password" onChange={handleChange} type="password" />
        <input name="password2" placeholder="Confirm Password" onChange={handleChange} type="password" />
        <button type="submit">Register</button>
      </form>

      {result && <p style={{ color: 'green' }}>회원가입 성공: {result.username}</p>}
      {error && <p style={{ color: 'red' }}>에러: {JSON.stringify(error)}</p>}
    </div>
  );
}

export default RegisterForm;
