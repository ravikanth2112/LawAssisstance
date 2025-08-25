import React, { useState } from 'react';
import { Upload, Save, Eye } from 'lucide-react';

const Branding = () => {
  const [firmName, setFirmName] = useState('Immigration Law Partners');
  const [tagline, setTagline] = useState('AI-Powered Assistant');
  const [primaryColor, setPrimaryColor] = useState('#3b82f6');
  const [secondaryColor, setSecondaryColor] = useState('#1e293b');

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ margin: '0 0 8px 0', fontSize: '28px', fontWeight: 'bold', color: '#1e293b' }}>
          Firm Branding
        </h1>
        <p style={{ margin: '0', color: '#64748b' }}>
          Customize your firm's branding and appearance
        </p>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '32px'
      }}>
        {/* Settings Panel */}
        <div>
          {/* Logo Section */}
          <div style={{
            backgroundColor: 'white',
            padding: '24px',
            borderRadius: '8px',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
            border: '1px solid #e2e8f0',
            marginBottom: '24px'
          }}>
            <h3 style={{ margin: '0 0 16px 0', fontSize: '18px', fontWeight: '600', color: '#1e293b' }}>
              Logo Upload
            </h3>
            <div style={{
              border: '2px dashed #e2e8f0',
              borderRadius: '8px',
              padding: '32px',
              textAlign: 'center',
              marginBottom: '16px'
            }}>
              <Upload size={32} style={{ color: '#64748b', marginBottom: '8px' }} />
              <p style={{ margin: '0 0 8px 0', color: '#1e293b', fontWeight: '500' }}>
                Upload your firm's logo
              </p>
              <p style={{ margin: '0', fontSize: '14px', color: '#64748b' }}>
                SVG, PNG, JPG up to 2MB
              </p>
            </div>
            <button style={{
              width: '100%',
              padding: '12px',
              backgroundColor: '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '500'
            }}>
              Choose File
            </button>
          </div>

          {/* Firm Information */}
          <div style={{
            backgroundColor: 'white',
            padding: '24px',
            borderRadius: '8px',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
            border: '1px solid #e2e8f0',
            marginBottom: '24px'
          }}>
            <h3 style={{ margin: '0 0 16px 0', fontSize: '18px', fontWeight: '600', color: '#1e293b' }}>
              Firm Information
            </h3>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px', fontWeight: '500', color: '#374151' }}>
                Firm Name
              </label>
              <input
                type="text"
                value={firmName}
                onChange={(e) => setFirmName(e.target.value)}
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #e2e8f0',
                  borderRadius: '6px',
                  fontSize: '14px'
                }}
              />
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px', fontWeight: '500', color: '#374151' }}>
                Tagline
              </label>
              <input
                type="text"
                value={tagline}
                onChange={(e) => setTagline(e.target.value)}
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #e2e8f0',
                  borderRadius: '6px',
                  fontSize: '14px'
                }}
              />
            </div>
          </div>

          {/* Color Scheme */}
          <div style={{
            backgroundColor: 'white',
            padding: '24px',
            borderRadius: '8px',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
            border: '1px solid #e2e8f0'
          }}>
            <h3 style={{ margin: '0 0 16px 0', fontSize: '18px', fontWeight: '600', color: '#1e293b' }}>
              Color Scheme
            </h3>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px', fontWeight: '500', color: '#374151' }}>
                Primary Color
              </label>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                <input
                  type="color"
                  value={primaryColor}
                  onChange={(e) => setPrimaryColor(e.target.value)}
                  style={{
                    width: '50px',
                    height: '40px',
                    border: '1px solid #e2e8f0',
                    borderRadius: '6px',
                    cursor: 'pointer'
                  }}
                />
                <input
                  type="text"
                  value={primaryColor}
                  onChange={(e) => setPrimaryColor(e.target.value)}
                  style={{
                    flex: 1,
                    padding: '12px',
                    border: '1px solid #e2e8f0',
                    borderRadius: '6px',
                    fontSize: '14px'
                  }}
                />
              </div>
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px', fontWeight: '500', color: '#374151' }}>
                Secondary Color
              </label>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                <input
                  type="color"
                  value={secondaryColor}
                  onChange={(e) => setSecondaryColor(e.target.value)}
                  style={{
                    width: '50px',
                    height: '40px',
                    border: '1px solid #e2e8f0',
                    borderRadius: '6px',
                    cursor: 'pointer'
                  }}
                />
                <input
                  type="text"
                  value={secondaryColor}
                  onChange={(e) => setSecondaryColor(e.target.value)}
                  style={{
                    flex: 1,
                    padding: '12px',
                    border: '1px solid #e2e8f0',
                    borderRadius: '6px',
                    fontSize: '14px'
                  }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Preview Panel */}
        <div>
          <div style={{
            backgroundColor: 'white',
            padding: '24px',
            borderRadius: '8px',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
            border: '1px solid #e2e8f0'
          }}>
            <h3 style={{ margin: '0 0 16px 0', fontSize: '18px', fontWeight: '600', color: '#1e293b' }}>
              Live Preview
            </h3>
            
            {/* Mock Sidebar Preview */}
            <div style={{
              backgroundColor: secondaryColor,
              color: 'white',
              padding: '20px',
              borderRadius: '8px',
              marginBottom: '16px'
            }}>
              <h4 style={{ 
                margin: '0 0 8px 0', 
                fontSize: '18px', 
                fontWeight: 'bold',
                color: primaryColor 
              }}>
                {firmName}
              </h4>
              <p style={{ margin: '0', fontSize: '14px', opacity: 0.8 }}>
                {tagline}
              </p>
            </div>

            {/* Mock Button Preview */}
            <div style={{ marginBottom: '16px' }}>
              <button style={{
                backgroundColor: primaryColor,
                color: 'white',
                border: 'none',
                padding: '12px 24px',
                borderRadius: '6px',
                fontSize: '14px',
                fontWeight: '500',
                marginRight: '8px'
              }}>
                Primary Button
              </button>
              <button style={{
                backgroundColor: 'transparent',
                color: primaryColor,
                border: `1px solid ${primaryColor}`,
                padding: '12px 24px',
                borderRadius: '6px',
                fontSize: '14px',
                fontWeight: '500'
              }}>
                Secondary Button
              </button>
            </div>

            {/* Mock Card Preview */}
            <div style={{
              border: `1px solid ${primaryColor}20`,
              borderRadius: '6px',
              padding: '16px',
              marginBottom: '16px'
            }}>
              <h5 style={{ 
                margin: '0 0 8px 0', 
                color: primaryColor,
                fontSize: '16px',
                fontWeight: '600'
              }}>
                Sample Card
              </h5>
              <p style={{ margin: '0', fontSize: '14px', color: '#64748b' }}>
                This is how your content cards will appear with the selected color scheme.
              </p>
            </div>

            <div style={{ display: 'flex', gap: '8px' }}>
              <button onClick={() => alert('Branding settings saved successfully!')} style={{
                flex: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                padding: '12px',
                backgroundColor: primaryColor,
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: '500'
              }}>
                <Save size={16} />
                Save Changes
              </button>
              <button style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                padding: '12px',
                backgroundColor: 'white',
                color: '#64748b',
                border: '1px solid #e2e8f0',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: '500'
              }}>
                <Eye size={16} />
                Preview
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Branding;
