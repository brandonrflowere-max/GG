<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>Magic Defender — строй забор, сражайся с тенями</title>
<style>
    * {
        user-select: none;
        touch-action: none;
        -webkit-tap-highlight-color: transparent;
    }
    body {
        margin: 0;
        overflow: hidden;
        background: #0a0f1a;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    canvas {
        display: block;
        width: 100%;
        height: 100%;
    }
    /* UI панель */
    #ui {
        position: absolute;
        top: 15px;
        left: 15px;
        right: 15px;
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
        pointer-events: none;
        z-index: 20;
        color: white;
        text-shadow: 1px 1px 0 #00000080;
    }
    .panel {
        background: rgba(0, 0, 0, 0.65);
        backdrop-filter: blur(8px);
        border-radius: 30px;
        padding: 8px 16px;
        display: flex;
        gap: 12px;
        font-weight: bold;
        font-size: 14px;
    }
    .stat {
        background: rgba(255,255,255,0.15);
        padding: 4px 12px;
        border-radius: 40px;
        white-space: nowrap;
    }
    #hp-bar {
        width: 140px;
        height: 8px;
        background: #5a2e1e;
        border-radius: 10px;
        overflow: hidden;
        margin: 6px 0 0 0;
    }
    #hp-fill {
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, #f3a683, #ff6b4a);
        transition: width 0.1s;
    }
    /* Меню */
    #menu {
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at center, #142c3a, #030e0a);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 100;
        backdrop-filter: blur(4px);
    }
    .menu-card {
        background: rgba(0,0,0,0.85);
        border-radius: 48px;
        border: 2px solid #ffaa55;
        padding: 30px 25px;
        text-align: center;
        max-width: 85%;
        width: 320px;
        color: white;
        box-shadow: 0 0 40px rgba(0,0,0,0.5);
    }
    .menu-card h1 {
        font-size: 2.4rem;
        margin: 0 0 8px;
        color: #ffcf9a;
        text-shadow: 0 0 10px orange;
    }
    .menu-card button {
        background: linear-gradient(45deg, #ff7b00, #ffb347);
        border: none;
        padding: 14px 24px;
        border-radius: 40px;
        font-size: 1.4rem;
        font-weight: bold;
        color: white;
        width: 100%;
        margin-top: 20px;
        cursor: pointer;
        box-shadow: 0 0 15px rgba(255,120,0,0.6);
    }
    /* Джойстик */
    #joystick-area {
        position: absolute;
        left: 25px;
        bottom: 25px;
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: rgba(100,150,255,0.2);
        border: 2px solid rgba(100,180,255,0.6);
        z-index: 30;
    }
    #joystick-thumb {
        position: absolute;
        left: 35px;
        top: 35px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: rgba(0,120,255,0.85);
        border: 2px solid white;
        transition: transform 0.01s linear;
    }
    /* Кнопка стрельбы */
    #shoot-btn {
        position: absolute;
        right: 25px;
        bottom: 25px;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: radial-gradient(circle, #ff7733, #dd3300);
        border: 3px solid rgba(255,255,255,0.4);
        z-index: 30;
        box-shadow: 0 0 30px rgba(255,80,0,0.6);
        cursor: pointer;
        transition: transform 0.05s;
    }
    #shoot-btn:active {
        transform: scale(0.92);
    }
    /* Адаптив */
    @media (max-width: 600px) {
        .panel { padding: 6px 12px; gap: 8px; font-size: 12px; }
        .stat { padding: 2px 8px; }
        #joystick-area { width: 100px; height: 100px; left: 15px; bottom: 15px; }
        #joystick-thumb { width: 45px; height: 45px; left: 27px; top: 27px; }
        #shoot-btn { width: 75px; height: 75px; right: 15px; bottom: 15px; }
        #hp-bar { width: 100px; }
    }
    /* Скрытые элементы */
    .hidden { display: none !important; }
</style>
</head>
<body>

<div id="menu">
    <div class="menu-card">
        <h1>⚔️ MAGIC DEFENDER ⚔️</h1>
        <p>Строй забор магией, уничтожай теней</p>
        <p>✨ 2 магии → новый сегмент</p>
        <p>🎮 Джойстик + кнопка огня</p>
        <button id="start-game-btn">НАЧАТЬ</button>
    </div>
</div>

<div id="ui" class="hidden">
    <div class="panel">
        <div class="stat">✨ <span id="magic-val">0</span></div>
        <div class="stat">👹 <span id="enemies-val">0</span></div>
        <div class="stat">⭐ УР. <span id="level-val">1</span></div>
        <div class="stat">🧱 <span id="segments-val">0</span>/<span id="total-segments">24</span></div>
    </div>
    <div class="panel">
        <div>🏰 ЗАМОК <div id="hp-bar"><div id="hp-fill"></div></div><span id="castle-hp">100</span></div>
    </div>
</div>

<div id="joystick-area" class="hidden">
    <div id="joystick-thumb"></div>
</div>
<div id="shoot-btn" class="hidden"></div>

<script type="importmap">
{
    "imports": {
        "three": "https://unpkg.com/three@0.158.0/build/three.module.js",
        "CSS2DRenderer": "https://unpkg.com/three@0.158.0/examples/jsm/renderers/CSS2DRenderer.js"
    }
}
</script>

<script type="module">
import * as THREE from 'three';
import { CSS2DRenderer, CSS2DObject } from 'CSS2DRenderer';

// ------------------------------------------------------------------
// 1. ИНИЦИАЛИЗАЦИЯ СЦЕНЫ
// ------------------------------------------------------------------
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x08131c);
scene.fog = new THREE.FogExp2(0x08131c, 0.022);

const camera = new THREE.PerspectiveCamera(65, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 7, 11);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
document.body.appendChild(renderer.domElement);

const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(window.innerWidth, window.innerHeight);
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0px';
labelRenderer.domElement.style.left = '0px';
labelRenderer.domElement.style.pointerEvents = 'none';
document.body.appendChild(labelRenderer.domElement);

// ------------------------------------------------------------------
// 2. ОСВЕЩЕНИЕ
// ------------------------------------------------------------------
const ambient = new THREE.AmbientLight(0x404060, 0.65);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xfff5d1, 1.0);
sun.position.set(5, 12, 4);
sun.castShadow = true;
scene.add(sun);
const fillLight = new THREE.PointLight(0x6688aa, 0.5);
fillLight.position.set(-2, 4, -3);
scene.add(fillLight);
const rimLight = new THREE.PointLight(0xffaa77, 0.4);
rimLight.position.set(0, 3, 6);
scene.add(rimLight);
const magicGlow = new THREE.PointLight(0xff44ff, 2, 20);
magicGlow.position.set(0, 5, 0);
scene.add(magicGlow);

// ------------------------------------------------------------------
// 3. ОКРУЖЕНИЕ
// ------------------------------------------------------------------
const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(45, 45),
    new THREE.MeshStandardMaterial({ color: 0x2d5c34, roughness: 0.9 })
);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// Трава (инстансинг не делаем ради простоты, но ограничим количество)
const grassGeo = new THREE.CylinderGeometry(0.05, 0.1, 0.2, 3);
const grassMat = new THREE.MeshStandardMaterial({ color: 0x5a9e3e });
for (let i = 0; i < 800; i++) {
    const blade = new THREE.Mesh(grassGeo, grassMat);
    const angle = Math.random() * Math.PI * 2;
    const rad = 5 + Math.random() * 18;
    blade.position.x = Math.cos(angle) * rad;
    blade.position.z = Math.sin(angle) * rad;
    blade.position.y = -0.25;
    blade.castShadow = true;
    blade.scale.set(1, 0.7 + Math.random() * 0.8, 1);
    scene.add(blade);
}

// Замок
const castleGroup = new THREE.Group();
const base = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.8, 1.5, 8), new THREE.MeshStandardMaterial({ color: 0xb87c42, roughness: 0.35 }));
base.castShadow = true;
castleGroup.add(base);
const tower = new THREE.Mesh(new THREE.CylinderGeometry(1.0, 1.2, 1.2, 8), new THREE.MeshStandardMaterial({ color: 0xc98f4b }));
tower.position.y = 1.1;
tower.castShadow = true;
castleGroup.add(tower);
const roof = new THREE.Mesh(new THREE.ConeGeometry(1.1, 1.0, 8), new THREE.MeshStandardMaterial({ color: 0xaa5533 }));
roof.position.y = 1.7;
roof.castShadow = true;
castleGroup.add(roof);
const flag = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.8, 0.1), new THREE.MeshStandardMaterial({ color: 0xdd8866 }));
flag.position.set(0.7, 2.2, 0);
castleGroup.add(flag);
scene.add(castleGroup);
const castlePos = new THREE.Vector3(0, 0, 0);

// Зона сдачи магии (золотой круг)
const depositRing = new THREE.Mesh(new THREE.RingGeometry(1.8, 2.5, 32), new THREE.MeshStandardMaterial({ color: 0xffaa55, emissive: 0x552200, side: THREE.DoubleSide }));
depositRing.rotation.x = -Math.PI / 2;
depositRing.position.y = 0.06;
scene.add(depositRing);

// ------------------------------------------------------------------
// 4. ЗАБОР (24 сегмента)
// ------------------------------------------------------------------
const FENCE_SEGMENTS = 24;
const fenceRadius = 5.3;
let fenceHP = new Array(FENCE_SEGMENTS).fill(0);
let fenceBuilt = new Array(FENCE_SEGMENTS).fill(false);
let segmentsBuilt = 0;
const fenceMaxHP = 80;
let fenceMeshes = [];

function createFenceSegment(angle) {
    const x = Math.cos(angle) * fenceRadius;
    const z = Math.sin(angle) * fenceRadius;
    const group = new THREE.Group();
    const pillar = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.5, 0.5), new THREE.MeshStandardMaterial({ color: 0x8b5a2b, roughness: 0.7 }));
    pillar.castShadow = true;
    group.add(pillar);
    for (let i = 0; i < 3; i++) {
        const plank = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.18, 0.12), new THREE.MeshStandardMaterial({ color: 0xad7a3a }));
        plank.position.y = 0.2 + i * 0.45;
        plank.castShadow = true;
        group.add(plank);
    }
    group.position.set(x, 0.1, z);
    group.lookAt(0, 0.1, 0);
    return group;
}
for (let i = 0; i < FENCE_SEGMENTS; i++) {
    const angle = (i / FENCE_SEGMENTS) * Math.PI * 2;
    const seg = createFenceSegment(angle);
    seg.visible = false;
    scene.add(seg);
    fenceMeshes.push(seg);
}

// ------------------------------------------------------------------
// 5. ИГРОК (маг)
// ------------------------------------------------------------------
const playerGroup = new THREE.Group();
const body = new THREE.Mesh(new THREE.CylinderGeometry(0.48, 0.48, 0.95, 8), new THREE.MeshStandardMaterial({ color: 0x3c8fbf, emissive: 0x113355 }));
body.castShadow = true;
playerGroup.add(body);
const head = new THREE.Mesh(new THREE.SphereGeometry(0.42, 32, 32), new THREE.MeshStandardMaterial({ color: 0xf9e0a0 }));
head.position.y = 0.68;
playerGroup.add(head);
const hat = new THREE.Mesh(new THREE.ConeGeometry(0.54, 0.6, 8), new THREE.MeshStandardMaterial({ color: 0x5533aa }));
hat.position.y = 1.08;
playerGroup.add(hat);
const staff = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.13, 1.2, 6), new THREE.MeshStandardMaterial({ color: 0xccaa77 }));
staff.position.set(0.62, 0.2, 0.48);
staff.rotation.z = 0.45;
playerGroup.add(staff);
const orb = new THREE.Mesh(new THREE.SphereGeometry(0.2, 24, 24), new THREE.MeshStandardMaterial({ color: 0xffaa44, emissive: 0x442200, emissiveIntensity: 0.7 }));
orb.position.set(1.0, 0.62, 0.58);
playerGroup.add(orb);
scene.add(playerGroup);
const player = { pos: new THREE.Vector3(2, 0, 2), speed: 5.5, vel: new THREE.Vector2(0, 0) };

// ------------------------------------------------------------------
// 6. МАГИЧЕСКИЕ КРИСТАЛЛЫ
// ------------------------------------------------------------------
let magicItems = [];
function spawnMagic() {
    const crystal = new THREE.Mesh(new THREE.DodecahedronGeometry(0.32), new THREE.MeshStandardMaterial({ color: 0xffcc66, emissive: 0x552200, emissiveIntensity: 0.8, metalness: 0.6 }));
    crystal.castShadow = true;
    const angle = Math.random() * Math.PI * 2;
    const rad = 5.5 + Math.random() * 8;
    crystal.position.set(Math.cos(angle) * rad, 0.25, Math.sin(angle) * rad);
    scene.add(crystal);
    magicItems.push(crystal);
}

// ------------------------------------------------------------------
// 7. ВРАГИ (тени) с HP барами (CSS2D)
// ------------------------------------------------------------------
let enemies = [];
function createEnemy(x, z) {
    const group = new THREE.Group();
    const bodyEn = new THREE.Mesh(new THREE.SphereGeometry(0.58, 32, 32), new THREE.MeshStandardMaterial({ color: 0x3a2a1f, roughness: 0.5 }));
    bodyEn.castShadow = true;
    group.add(bodyEn);
    const eyeMat = new THREE.MeshStandardMaterial({ color: 0xff4444, emissive: 0xff1111, emissiveIntensity: 0.8 });
    const eyeL = new THREE.Mesh(new THREE.SphereGeometry(0.13, 24, 24), eyeMat);
    eyeL.position.set(-0.25, 0.28, 0.72);
    group.add(eyeL);
    const eyeR = new THREE.Mesh(new THREE.SphereGeometry(0.13, 24, 24), eyeMat);
    eyeR.position.set(0.25, 0.28, 0.72);
    group.add(eyeR);
    const hornL = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.55, 6), new THREE.MeshStandardMaterial({ color: 0x442200 }));
    hornL.position.set(-0.35, 0.62, 0.45);
    hornL.rotation.z = -0.35;
    group.add(hornL);
    const hornR = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.55, 6), new THREE.MeshStandardMaterial({ color: 0x442200 }));
    hornR.position.set(0.35, 0.62, 0.45);
    hornR.rotation.z = 0.35;
    group.add(hornR);
    group.position.set(x, 0, z);
    scene.add(group);
    // HP Bar CSS2D
    const div = document.createElement('div');
    div.style.width = '60px';
    div.style.height = '6px';
    div.style.background = '#800';
    div.style.borderRadius = '3px';
    const fillDiv = document.createElement('div');
    fillDiv.style.height = '100%';
    fillDiv.style.width = '100%';
    fillDiv.style.background = '#0f0';
    fillDiv.style.borderRadius = '3px';
    div.appendChild(fillDiv);
    const label = new CSS2DObject(div);
    label.position.copy(group.position);
    label.position.y += 1.1;
    scene.add(label);
    return { mesh: group, hp: 100, maxHp: 100, hpLabel: label, hpFill: fillDiv, pos: new THREE.Vector3(x, 0, z) };
}

function spawnEnemy() {
    const angle = Math.random() * Math.PI * 2;
    const rad = 10 + Math.random() * 4;
    const x = Math.cos(angle) * rad;
    const z = Math.sin(angle) * rad;
    enemies.push(createEnemy(x, z));
}

// ------------------------------------------------------------------
// 8. МЕХАНИКИ ЗАБОРА
// ------------------------------------------------------------------
function buildNextSegment() {
    if (segmentsBuilt >= FENCE_SEGMENTS) return false;
    if (playerMagic >= 2) {
        playerMagic -= 2;
        const idx = segmentsBuilt;
        fenceHP[idx] = fenceMaxHP;
        fenceBuilt[idx] = true;
        fenceMeshes[idx].visible = true;
        segmentsBuilt++;
        addEffect(castlePos.x, castlePos.z, 0x88ff88);
        showMessage(`🏗️ Сегмент ${segmentsBuilt}/${FENCE_SEGMENTS} построен!`, 1.2);
        updateUI();
        return true;
    }
    return false;
}
function repairSegment(idx) {
    if (fenceHP[idx] > 0 && fenceHP[idx] < fenceMaxHP && playerMagic >= 1) {
        playerMagic--;
        fenceHP[idx] = Math.min(fenceMaxHP, fenceHP[idx] + 1);
        const t = fenceHP[idx] / fenceMaxHP;
        const newColor = new THREE.Color().setHSL(0.10, 1, 0.2 + t * 0.5);
        fenceMeshes[idx].children.forEach(c => { if (c.isMesh) c.material.color = newColor; });
        updateUI();
        return true;
    }
    return false;
}
function autoDeposit() {
    if (!gameActive) return;
    const dist = player.pos.distanceTo(castlePos);
    if (dist < 2.2 && playerMagic > 0) {
        if (segmentsBuilt < FENCE_SEGMENTS) {
            buildNextSegment();
            return;
        }
        for (let i = 0; i < FENCE_SEGMENTS; i++) {
            if (fenceHP[i] > 0 && fenceHP[i] < fenceMaxHP) {
                repairSegment(i);
                return;
            }
        }
    }
}

// ------------------------------------------------------------------
// 9. СТРЕЛЬБА (огненные шары)
// ------------------------------------------------------------------
let bullets = [];
function shoot() {
    if (!gameActive || enemies.length === 0) return;
    let closest = null, minDist = Infinity;
    for (let e of enemies) {
        const d = player.pos.distanceTo(e.mesh.position);
        if (d < minDist) {
            minDist = d;
            closest = e;
        }
    }
    if (!closest) return;
    const ball = new THREE.Mesh(new THREE.SphereGeometry(0.28, 16, 16), new THREE.MeshStandardMaterial({ color: 0xff6600, emissive: 0xff3300, emissiveIntensity: 0.9 }));
    scene.add(ball);
    const start = player.pos.clone();
    const end = closest.mesh.position.clone();
    let progress = 0;
    function animateBall() {
        progress += 0.07;
        if (progress >= 1) {
            scene.remove(ball);
            closest.hp -= 34;
            addEffect(end.x, end.z, 0xff5500);
            if (closest.hp <= 0) {
                scene.remove(closest.mesh);
                scene.remove(closest.hpLabel);
                enemies.splice(enemies.indexOf(closest), 1);
                kills++;
                if (kills % 3 === 0) {
                    level++;
                    updateUI();
                    showMessage(`⭐ УРОВЕНЬ ${level}!`, 1.5);
                }
                updateUI();
            } else {
                const percent = (closest.hp / closest.maxHp) * 100;
                closest.hpFill.style.width = percent + "%";
            }
            return;
        }
        const t = progress;
        const x = start.x + (end.x - start.x) * t;
        const z = start.z + (end.z - start.z) * t;
        ball.position.set(x, 0.5 + Math.sin(t * Math.PI) * 1.2, z);
        requestAnimationFrame(animateBall);
    }
    animateBall();
}

// ------------------------------------------------------------------
// 10. ЧАСТИЦЫ (эффекты)
// ------------------------------------------------------------------
let particles = [];
function addEffect(x, z, color) {
    for (let i = 0; i < 12; i++) {
        const p = new THREE.Mesh(new THREE.SphereGeometry(0.1, 6, 6), new THREE.MeshStandardMaterial({ color, emissive: color }));
        p.position.set(x, 0.2, z);
        p.userData = { vel: new THREE.Vector3((Math.random() - 0.5) * 2.5, Math.random() * 2, (Math.random() - 0.5) * 2.5), life: 0.7 };
        scene.add(p);
        particles.push(p);
    }
}
function updateParticles(delta) {
    for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.userData.life -= delta * 1.5;
        if (p.userData.life <= 0) {
            scene.remove(p);
            particles.splice(i, 1);
            i--;
            continue;
        }
        p.userData.vel.y -= 3 * delta;
        p.position.x += p.userData.vel.x * delta;
        p.position.z += p.userData.vel.z * delta;
        p.position.y += p.userData.vel.y * delta;
        p.scale.setScalar(p.userData.life);
    }
}

// ------------------------------------------------------------------
// 11. ИГРОВОЕ СОСТОЯНИЕ
// ------------------------------------------------------------------
let gameActive = false;
let hp = 100;
let kills = 0;
let level = 1;
let playerMagic = 0;
let spawnFrame = 0;
const ENEMY_SPAWN_DELAY = 100; // кадры

function updateUI() {
    if (!gameActive) return;
    document.getElementById('magic-val').innerText = playerMagic;
    document.getElementById('enemies-val').innerText = enemies.length;
    document.getElementById('level-val').innerText = level;
    document.getElementById('segments-val').innerText = segmentsBuilt;
    document.getElementById('total-segments').innerText = FENCE_SEGMENTS;
    document.getElementById('castle-hp').innerText = Math.floor(hp);
    document.getElementById('hp-fill').style.width = (hp / 100) * 100 + "%";
}
function showMessage(text, dur) {
    const div = document.createElement('div');
    div.textContent = text;
    div.style.position = 'absolute';
    div.style.bottom = '120px';
    div.style.left = '50%';
    div.style.transform = 'translateX(-50%)';
    div.style.backgroundColor = 'rgba(0,0,0,0.8)';
    div.style.color = '#ffec9f';
    div.style.padding = '6px 18px';
    div.style.borderRadius = '40px';
    div.style.fontWeight = 'bold';
    div.style.zIndex = '100';
    div.style.pointerEvents = 'none';
    document.body.appendChild(div);
    setTimeout(() => div.remove(), dur * 1000);
}

// ------------------------------------------------------------------
// 12. ОБНОВЛЕНИЕ ВРАГОВ (с учётом забора)
// ------------------------------------------------------------------
function updateEnemies(delta) {
    const speed = 1.3 + level * 0.08;
    for (let i = 0; i < enemies.length; i++) {
        const e = enemies[i];
        const dir = new THREE.Vector3().subVectors(player.pos, e.mesh.position).normalize();
        e.mesh.position.x += dir.x * speed * delta;
        e.mesh.position.z += dir.z * speed * delta;
        e.mesh.lookAt(player.pos);
        e.hpLabel.position.copy(e.mesh.position);
        e.hpLabel.position.y += 1.1;
        e.pos.copy(e.mesh.position);
        const distToCenter = e.mesh.position.length();
        // Атака забора
        if (distToCenter < fenceRadius + 0.5) {
            let angle = Math.atan2(e.mesh.position.z, e.mesh.position.x);
            if (angle < 0) angle += Math.PI * 2;
            const segIdx = Math.floor(angle / (Math.PI * 2 / FENCE_SEGMENTS));
            if (fenceHP[segIdx] > 0) {
                fenceHP[segIdx] = Math.max(0, fenceHP[segIdx] - 1);
                if (fenceHP[segIdx] === 0) {
                    fenceBuilt[segIdx] = false;
                    fenceMeshes[segIdx].visible = false;
                    segmentsBuilt--;
                } else {
                    const t = fenceHP[segIdx] / fenceMaxHP;
                    const newColor = new THREE.Color().setHSL(0.10, 1, 0.2 + t * 0.5);
                    fenceMeshes[segIdx].children.forEach(c => { if (c.isMesh) c.material.color = newColor; });
                }
                addEffect(e.mesh.position.x, e.mesh.position.z, 0xff8866);
                scene.remove(e.mesh);
                scene.remove(e.hpLabel);
                enemies.splice(i, 1);
                i--;
                continue;
            }
        }
        // Атака замка
        if (e.mesh.position.distanceTo(castlePos) < 1.8) {
            hp -= 1;
            addEffect(castlePos.x, castlePos.z, 0xff4444);
            scene.remove(e.mesh);
            scene.remove(e.hpLabel);
            enemies.splice(i, 1);
            i--;
            updateUI();
            if (hp <= 0) {
                gameActive = false;
                showMessage("GAME OVER", 2);
                setTimeout(() => location.reload(), 2500);
            }
        }
    }
}

// ------------------------------------------------------------------
// 13. СБОР КРИСТАЛЛОВ
// ------------------------------------------------------------------
function collectMagic(delta) {
    for (let i = 0; i < magicItems.length; i++) {
        const c = magicItems[i];
        c.rotation.y += delta * 3;
        if (c.position.distanceTo(player.pos) < 1.0) {
            playerMagic++;
            addEffect(c.position.x, c.position.z, 0xffcc55);
            scene.remove(c);
            magicItems.splice(i, 1);
            i--;
            updateUI();
            showMessage("✨ +1 магия", 0.5);
        }
    }
}

// ------------------------------------------------------------------
// 14. УПРАВЛЕНИЕ: ДЖОЙСТИК + КЛАВИАТУРА
// ------------------------------------------------------------------
let joyActive = false;
let joyX = 0, joyY = 0;
const joyArea = document.getElementById('joystick-area');
const joyThumb = document.getElementById('joystick-thumb');

function handleJoyMove(e) {
    if (!joyActive) return;
    const touch = e.touches ? e.touches[0] : e;
    const rect = joyArea.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    let dx = touch.clientX - cx;
    let dy = touch.clientY - cy;
    const max = 45;
    const dist = Math.hypot(dx, dy);
    if (dist > max) {
        dx = dx / dist * max;
        dy = dy / dist * max;
    }
    joyX = dx / max;
    joyY = dy / max;
    joyThumb.style.transform = `translate(${dx}px, ${dy}px)`;
}
function handleJoyEnd() {
    joyActive = false;
    joyX = joyY = 0;
    joyThumb.style.transform = `translate(0px, 0px)`;
}
joyArea.addEventListener('touchstart', (e) => { joyActive = true; e.preventDefault(); });
window.addEventListener('touchmove', handleJoyMove);
window.addEventListener('touchend', handleJoyEnd);
joyArea.addEventListener('mousedown', () => joyActive = true);
window.addEventListener('mousemove', handleJoyMove);
window.addEventListener('mouseup', handleJoyEnd);

// Клавиатура ПК (для отладки, но в Google Play не нужна, но оставим)
const keys = { w: false, s: false, a: false, d: false, up: false, down: false, left: false, right: false };
window.addEventListener('keydown', (e) => {
    const k = e.key.toLowerCase();
    if (k === 'w') keys.w = true;
    if (k === 's') keys.s = true;
    if (k === 'a') keys.a = true;
    if (k === 'd') keys.d = true;
    if (k === 'arrowup') keys.up = true;
    if (k === 'arrowdown') keys.down = true;
    if (k === 'arrowleft') keys.left = true;
    if (k === 'arrowright') keys.right = true;
    if (k === ' ' || k === 'space') { e.preventDefault(); shoot(); }
});
window.addEventListener('keyup', (e) => {
    const k = e.key.toLowerCase();
    if (k === 'w') keys.w = false;
    if (k === 's') keys.s = false;
    if (k === 'a') keys.a = false;
    if (k === 'd') keys.d = false;
    if (k === 'arrowup') keys.up = false;
    if (k === 'arrowdown') keys.down = false;
    if (k === 'arrowleft') keys.left = false;
    if (k === 'arrowright') keys.right = false;
});

document.getElementById('shoot-btn').addEventListener('click', shoot);
document.getElementById('shoot-btn').addEventListener('touchstart', (e) => { e.preventDefault(); shoot(); });

function updatePlayerMovement(delta) {
    let mx = joyX;
    let mz = joyY;
    if (keys.w || keys.up) mz -= 1;
    if (keys.s || keys.down) mz += 1;
    if (keys.a || keys.left) mx -= 1;
    if (keys.d || keys.right) mx += 1;
    if (Math.abs(mx) > 1) mx = Math.sign(mx);
    if (Math.abs(mz) > 1) mz = Math.sign(mz);
    player.pos.x += mx * player.speed * delta;
    player.pos.z += mz * player.speed * delta;
    const limit = 23;
    player.pos.x = Math.min(limit, Math.max(-limit, player.pos.x));
    player.pos.z = Math.min(limit, Math.max(-limit, player.pos.z));
    playerGroup.position.copy(player.pos);
    playerGroup.position.y = 0.1 + Math.sin(Date.now() * 0.01) * 0.05;
    if (Math.abs(mx) > 0.05 || Math.abs(mz) > 0.05) {
        playerGroup.rotation.y = Math.atan2(mx, mz);
    }
}

// ------------------------------------------------------------------
// 15. ЗАПУСК ИГРЫ
// ------------------------------------------------------------------
function startGame() {
    gameActive = true;
    document.getElementById('menu').classList.add('hidden');
    document.getElementById('ui').classList.remove('hidden');
    document.getElementById('joystick-area').classList.remove('hidden');
    document.getElementById('shoot-btn').classList.remove('hidden');
    // Сброс параметров
    hp = 100;
    kills = 0;
    level = 1;
    playerMagic = 0;
    segmentsBuilt = 0;
    for (let i = 0; i < FENCE_SEGMENTS; i++) {
        fenceHP[i] = 0;
        fenceBuilt[i] = false;
        fenceMeshes[i].visible = false;
    }
    enemies.forEach(e => { scene.remove(e.mesh); scene.remove(e.hpLabel); });
    magicItems.forEach(m => scene.remove(m));
    enemies = [];
    magicItems = [];
    bullets = [];
    particles = [];
    player.pos.set(2, 0, 2);
    for (let i = 0; i < 6; i++) spawnMagic();
    for (let i = 0; i < 3; i++) spawnEnemy();
    updateUI();
    showMessage("Собирай магию и строй забор у замка!", 2);
}
document.getElementById('start-game-btn').onclick = startGame;

// ------------------------------------------------------------------
// 16. АНИМАЦИОННЫЙ ЦИКЛ
// ------------------------------------------------------------------
let lastTime = performance.now();
function animate() {
    const now = performance.now();
    let delta = Math.min(0.033, (now - lastTime) / 1000);
    lastTime = now;
    if (gameActive) {
        updatePlayerMovement(delta);
        collectMagic(delta);
        autoDeposit();
        updateEnemies(delta);
        updateParticles(delta);
        spawnFrame++;
        if (spawnFrame >= ENEMY_SPAWN_DELAY && enemies.length < 12) {
            spawnFrame = 0;
            spawnEnemy();
        }
        if (Math.random() < 0.018 && magicItems.length < 15) spawnMagic();
        camera.position.x += (player.pos.x - camera.position.x) * 0.08;
        camera.position.z += ((player.pos.z + 9) - camera.position.z) * 0.08;
        camera.lookAt(player.pos);
        magicGlow.intensity = 2 + Math.sin(Date.now() * 0.003) * 1.2;
    }
    renderer.render(scene, camera);
    labelRenderer.render(scene, camera);
    requestAnimationFrame(animate);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    labelRenderer.setSize(window.innerWidth, window.innerHeight);
});
</script>
</body>
</html>