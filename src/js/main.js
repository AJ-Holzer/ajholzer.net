// ========================= //
//  Copyright (c) AJ-Holzer  //
//  All rights reserved      //
// ========================= //

const canvas = document.getElementById("liquid-bg");
const ctx = canvas.getContext("2d", { alpha: true });

// ==========================
// CONFIG
// ==========================
const BASE_PARTICLE_COUNT = 45;
const MAX_DPR = 1.5; // cap DPR to avoid killing mobile GPUs
const SPEED_SCALE = 0.6; // slows movement slightly (smoother on mobile)

// ==========================
// STATE
// ==========================
let width = 0;
let height = 0;
let dpr = Math.min(window.devicePixelRatio || 1, MAX_DPR);
let particles = [];
let lastTime = performance.now();

// ==========================
// RESIZE (debounced)
// ==========================
let resizeTimeout;
function resize() {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    dpr = Math.min(window.devicePixelRatio || 1, MAX_DPR);

    width = Math.floor(window.innerWidth);
    height = Math.floor(window.innerHeight);

    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);

    canvas.style.width = width + "px";
    canvas.style.height = height + "px";

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    adjustParticleCount();
  }, 100);
}

window.addEventListener("resize", resize, { passive: true });
resize();

// ==========================
// PARTICLE CLASS
// ==========================
class Particle {
  constructor() {
    this.reset();
  }

  reset() {
    this.radius = 80 + Math.random() * 120;

    this.x = Math.random() * width;
    this.y = Math.random() * height;

    this.speedX = (Math.random() - 0.5) * 0.2 * SPEED_SCALE;
    this.speedY = (Math.random() - 0.5) * 0.2 * SPEED_SCALE;

    this.hue = 170 + Math.random() * 20;

    // pre-render gradient ONCE
    this.gradient = this.createGradient();
  }

  createGradient() {
    const g = ctx.createRadialGradient(0, 0, 0, 0, 0, this.radius);

    g.addColorStop(0, `hsla(${this.hue}, 70%, 60%, 0.12)`);
    g.addColorStop(0.5, `hsla(${this.hue}, 70%, 60%, 0.06)`);
    g.addColorStop(1, "transparent");

    return g;
  }

  update(dt) {
    this.x += this.speedX * dt;
    this.y += this.speedY * dt;

    if (
      this.x < -this.radius ||
      this.x > width + this.radius ||
      this.y < -this.radius ||
      this.y > height + this.radius
    ) {
      this.reset();
    }
  }

  draw() {
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.fillStyle = this.gradient;
    ctx.beginPath();
    ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }
}

// ==========================
// PARTICLE COUNT SCALING
// ==========================
function adjustParticleCount() {
  const isMobile = width < 768;
  const targetCount = isMobile
    ? Math.floor(BASE_PARTICLE_COUNT * 0.8)
    : BASE_PARTICLE_COUNT;

  if (particles.length > targetCount) {
    particles.length = targetCount;
  } else {
    while (particles.length < targetCount) {
      particles.push(new Particle());
    }
  }
}

// ==========================
// ANIMATION LOOP (time-based)
// ==========================
function animate(now) {
  const dt = Math.min(now - lastTime, 32); // clamp delta
  lastTime = now;

  ctx.clearRect(0, 0, width, height);

  for (let i = 0; i < particles.length; i++) {
    particles[i].update(dt);
    particles[i].draw();
  }

  requestAnimationFrame(animate);
}

requestAnimationFrame(animate);
