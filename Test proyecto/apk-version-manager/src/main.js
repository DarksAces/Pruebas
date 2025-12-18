import './style.css'

const app = document.querySelector('#app');

// State
let currentState = 'idle'; // idle, selected, processing, success
let currentFile = null;

const render = () => {
  app.innerHTML = '';
  
  const container = document.createElement('div');
  container.className = 'glass-card';
  
  // Header
  const header = document.createElement('div');
  header.className = 'header';
  header.innerHTML = `
    <h1>APK Builder</h1>
    <p>Drag & drop your APK or AAB file to create a new version</p>
  `;
  container.appendChild(header);

  // Content based on state
  const content = document.createElement('div');
  content.className = 'content';

  if (currentState === 'idle') {
    content.innerHTML = `
      <div class="drop-zone" id="dropZone">
        <input type="file" id="fileInput" class="file-input" accept=".apk,.aab" />
        <div class="icon-container">
          <i data-lucide="upload-cloud" width="48" height="48"></i>
        </div>
        <h3>Drop file here</h3>
        <p>Supports .APK and .AAB</p>
      </div>
    `;
  } else if (currentState === 'selected') {
    const isAab = currentFile.name.endsWith('.aab');
    const sizeMb = (currentFile.size / (1024 * 1024)).toFixed(2);
    
    content.innerHTML = `
      <div class="file-info">
        <div class="file-icon">
          <i data-lucide="${isAab ? 'package' : 'smartphone'}" width="40" height="40"></i>
        </div>
        <div class="file-details">
          <h3>${currentFile.name}</h3>
          <p>${sizeMb} MB • ${isAab ? 'Android App Bundle' : 'Android Package'}</p>
        </div>
        
        ${isAab ? `
        <div class="aab-notice" style="background: rgba(236, 72, 153, 0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(236, 72, 153, 0.3); width: 100%;">
          <div style="display:flex; align-items:center; gap: 0.5rem; color: #f9a8d4; margin-bottom: 0.5rem;">
            <i data-lucide="link" width="16"></i>
            <strong>Requires Linking</strong>
          </div>
          <p style="font-size: 0.85rem; color: #cbd5e1;">This AAB will be processed with bundletool to generate a universal APK.</p>
        </div>
        ` : ''}

        <div class="actions">
          <button class="btn btn-secondary" id="cancelBtn">Cancel</button>
          <button class="btn btn-primary" id="processBtn">
            <i data-lucide="zap" width="18"></i>
            ${isAab ? 'Link & Build' : 'Create New Version'}
          </button>
        </div>
      </div>
    `;
  } else if (currentState === 'processing') {
    content.innerHTML = `
      <div class="status-area">
        <div class="processing-indicator">
          <div class="spinner"></div>
          <h3>Processing ${currentFile.name}...</h3>
          <p id="processStep">Initializing build environment...</p>
        </div>
      </div>
    `;
  } else if (currentState === 'success') {
     content.innerHTML = `
      <div class="success-message">
        <div class="success-icon">
           <i data-lucide="check" width="32"></i>
        </div>
        <h3>Build Successful!</h3>
        <p>New version v1.0.1 created.</p>
        
        <div class="actions">
          <button class="btn btn-secondary" id="resetBtn">Build Another</button>
          <button class="btn btn-primary">
            <i data-lucide="download" width="18"></i>
            Download APK
          </button>
        </div>
      </div>
    `;
  }

  container.appendChild(content);
  app.appendChild(container);
  
  // Re-run icons
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // Bind Events
  if (currentState === 'idle') {
    bindDropZone();
  } else if (currentState === 'selected') {
    document.getElementById('cancelBtn').addEventListener('click', reset);
    document.getElementById('processBtn').addEventListener('click', startProcess);
  } else if (currentState === 'success') {
    document.getElementById('resetBtn').addEventListener('click', reset);
  }
};

// Logic
const reset = () => {
  currentState = 'idle';
  currentFile = null;
  render();
};

const handleFile = (file) => {
  if (file && (file.name.endsWith('.apk') || file.name.endsWith('.aab'))) {
    currentFile = file;
    currentState = 'selected';
    render();
  } else {
    alert('Please upload a valid .apk or .aab file');
  }
};

const bindDropZone = () => {
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');

  dropZone.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
  });

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    if (e.dataTransfer.files.length) {
      handleFile(e.dataTransfer.files[0]);
    }
  });
};

const startProcess = () => {
  currentState = 'processing';
  render();
  
  const steps = currentFile.name.endsWith('.aab') 
    ? ['Analysing Bundle...', 'Linking Resources...', 'Generating Universal APK...', 'Signing Package...']
    : ['Decompiling...', 'Updating Version Code...', 'Recompiling...', 'Aligning Zip...'];
    
  let stepIndex = 0;
  
  const interval = setInterval(() => {
    const stepEl = document.getElementById('processStep');
    if (stepEl) {
       stepEl.innerText = steps[stepIndex];
    }
    stepIndex++;
    
    if (stepIndex >= steps.length) {
      clearInterval(interval);
      setTimeout(() => {
        currentState = 'success';
        render();
      }, 800);
    }
  }, 1500);
};

// Init
render();
