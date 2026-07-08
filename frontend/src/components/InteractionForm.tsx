import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import type { RootState } from '../store';
import { updateForm } from '../store/interactionSlice';

const InteractionForm: React.FC = () => {
  const dispatch = useDispatch();
  const form = useSelector((state: RootState) => state.interaction.currentForm);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    dispatch(updateForm({ [e.target.name]: e.target.value }));
  };

  return (
    <div className="glass-panel left-panel">
      <h2 style={{ marginBottom: '1rem', color: 'var(--primary)', fontWeight: 600 }}>Interaction Details</h2>
      
      <div className="form-grid">
        <div className="form-group">
          <label>HCP Name</label>
          <input 
            name="hcp_name" 
            placeholder="Search or select HCP..." 
            value={form.hcp_name} 
            onChange={handleChange} 
          />
        </div>

        <div className="form-group">
          <label>Interaction Type</label>
          <select name="interaction_type" value={form.interaction_type} onChange={handleChange}>
            <option>Meeting</option>
            <option>Call</option>
            <option>Email</option>
            <option>Event</option>
          </select>
        </div>

        <div className="form-group">
          <label>Date</label>
          <input 
            type="date" 
            name="date" 
            value={form.date} 
            onChange={handleChange} 
          />
        </div>

        <div className="form-group">
          <label>Time</label>
          <input 
            type="time" 
            name="time" 
            value={form.time} 
            onChange={handleChange} 
          />
        </div>

        <div className="form-group full-width">
          <label>Attendees</label>
          <input 
            name="attendees" 
            placeholder="Enter names or search..." 
            value={form.attendees} 
            onChange={handleChange} 
          />
        </div>

        <div className="form-group full-width">
          <label>Topics Discussed</label>
          <textarea 
            name="topics" 
            rows={3} 
            placeholder="Enter key discussion points..." 
            value={form.topics} 
            onChange={handleChange} 
          />
        </div>

        <div className="form-group full-width">
          <label>Materials Shared / Samples Distributed</label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <input 
              name="materials" 
              placeholder="Materials added..." 
              value={form.materials} 
              onChange={handleChange} 
            />
            <input 
              name="samples" 
              placeholder="Samples added..." 
              value={form.samples} 
              onChange={handleChange} 
            />
          </div>
        </div>

        <div className="form-group full-width">
          <label>Observed/Inferred HCP Sentiment</label>
          <div style={{ display: 'flex', gap: '1.5rem', marginTop: '0.5rem' }}>
            {['Positive', 'Neutral', 'Negative'].map(sent => (
              <label key={sent} style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', cursor: 'pointer', margin: 0, fontWeight: 400, color: 'var(--text-main)' }}>
                <input 
                  type="radio" 
                  name="sentiment" 
                  value={sent} 
                  checked={form.sentiment === sent}
                  onChange={handleChange}
                  style={{ width: 'auto' }}
                />
                {sent}
              </label>
            ))}
          </div>
        </div>

        <div className="form-group full-width">
          <label>Outcomes</label>
          <textarea 
            name="outcomes" 
            rows={2} 
            placeholder="Key outcomes or agreements..." 
            value={form.outcomes} 
            onChange={handleChange} 
          />
        </div>

        <div className="form-group full-width">
          <label>Follow-up Actions</label>
          <textarea 
            name="follow_up" 
            rows={2} 
            placeholder="Enter next steps or tasks..." 
            value={form.follow_up} 
            onChange={handleChange} 
          />
        </div>
      </div>
    </div>
  );
};

export default InteractionForm;
