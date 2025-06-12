import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [goals, setGoals] = useState([]);
  const [title, setTitle] = useState('');
  const [deadline, setDeadline] = useState('');

  const fetchGoals = async () => {
    const res = await axios.get('http://localhost:5000/api/goals');
    setGoals(res.data);
  };

  const addGoal = async () => {
    await axios.post('http://localhost:5000/api/goals', { title, deadline });
    fetchGoals();
  };

  useEffect(() => {
    fetchGoals();
  }, []);

  return (
    <div>
      <h1>학습 목표 설정</h1>
      <input placeholder="목표" value={title} onChange={(e) => setTitle(e.target.value)} />
      <input type="date" value={deadline} onChange={(e) => setDeadline(e.target.value)} />
      <button onClick={addGoal}>추가</button>
      <ul>
        {goals.map(([id, t, d]) => (
          <li key={id}>{t} - {d}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
