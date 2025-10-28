// src/app/page.tsx
"use client";
import { IconBacklog, IconMatrix, IconKanban, IconAvailability } from "@/components/NeusiIcons";
import Script from "next/script";
import { useEffect, useState } from "react";
import Image from "next/image";
import { me, logout } from "@/lib/api";
import { useRouter } from "next/navigation";
import "./home.css";

type User = { username: string; is_authenticated: boolean };

export default function Home() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const u = await me();
        if (!u?.is_authenticated) {
          router.replace("/login");
          return;
        }
        if (mounted) setUser(u);
      } catch {
        router.replace("/login");
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => {
      mounted = false;
    };
  }, [router]);

  // Fondo dinámico (polygons) – versión ligera
  useEffect(() => {
    const cleanup = makePolygonsBackground();
    return () => cleanup?.();
  }, []);

  async function onLogout() {
    try {
      await logout();
      router.replace("/login");
    } catch (e: any) {
      setErr(e?.message || "No se pudo cerrar sesión");
    }
  }

  if (loading) return <p className="home-loading">Cargando…</p>;
  if (!user) return null;

  return (
    <main className="home-root">
      {/* Topbar */}
      <header className="home-topbar">
        <div className="brand">
          {/* Asegúrate de tener /public/neusi-logo.png */}
          <img
            src="/backlog/img/logo.png"
            alt="NEUSI"
            width={36}
            height={36}
            className="brand-logo"
            onError={(e) => {
              // Fallback visual si falta el logo
              (e.target as HTMLImageElement).style.display = "none";
              const fallback = document.getElementById("brand-fallback");
              if (fallback) fallback.style.display = "grid";
            }}
          />
          <span id="brand-fallback" className="brand-fallback">N</span>
          <span className="brand-title">NEUSI · Task Manager</span>
        </div>

        <div className="top-actions">
          <span className="hello">Hola, <b>{user.username}</b></span>
          <button className="btn-ghost" onClick={onLogout} aria-label="Cerrar sesión">
            Cerrar sesión
          </button>
        </div>
      </header>

      {/* Hero */}
      <section className="home-hero">
        <h1>Bienvenido a NEUSI Task Manager</h1>
        <p>Organiza el trabajo del equipo, visualiza el progreso y centraliza la ejecución. Todo en un mismo lugar.</p>
      </section>

      {/* Tiles principales */}
  {/* añade este Script opcional (móvil) */}
  <Script src="/tiles-hover.js" strategy="afterInteractive" />

  {/* ...topbar y hero existentes... */}

  <section className="tiles tiles--cover">
    <a className="tile tile--blue cover" href="/backlog">
      <div className="tile-face tile-face--icon">
        <IconBacklog className="ico" />
      </div>
      <div className="tile-face tile-face--text">
        <h3>Backlog</h3>
        <p>Gestión de tareas y prioridades.</p>
      </div>
    </a>

    <a className="tile tile--green cover" href="/matriz">
      <div className="tile-face tile-face--icon">
        <IconMatrix className="ico" />
      </div>
      <div className="tile-face tile-face--text">
        <h3>Matriz</h3>
        <p>Urgente/Importante para foco.</p>
      </div>
    </a>

    <a className="tile tile--purple cover" href="/kanban">
      <div className="tile-face tile-face--icon">
        <IconKanban className="ico" />
      </div>
      <div className="tile-face tile-face--text">
        <h3>Kanban</h3>
        <p>Flujo visual por estados.</p>
      </div>
    </a>

    <a className="tile tile--teal cover" href="/disponibilidad">
      <div className="tile-face tile-face--icon">
        <IconAvailability className="ico" />
      </div>
      <div className="tile-face tile-face--text">
        <h3>Disponibilidad</h3>
        <p>Planifica la semana del equipo.</p>
      </div>
    </a>
  </section>
      {/* Acceso rápido */}
      <section className="quick">
        <div className="quick-head">
          <span className="quick-emoji" aria-hidden>-</span>
          <h2>Acceso Rápido</h2>
        </div>

        <div className="chips">
          <a className="chip" href="/daily/personal">Mi Daily de hoy</a>
          <a className="chip" href="/kanban">Kanban de mis tareas</a>
          <a className="chip" href="/disponibilidad">Mi horario semanal</a>
        </div>
      </section>

      {err && <p className="err">{err}</p>}
    </main>
  );
}

/* ===== Fondo “polygons” mínimo (limpio y eficiente) ===== */
function makePolygonsBackground() {
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d")!;
  canvas.className = "bg-canvas";
  document.body.appendChild(canvas);

  let DPR = Math.min(2, window.devicePixelRatio || 1);
  let W = (canvas.width = Math.floor(window.innerWidth * DPR));
  let H = (canvas.height = Math.floor(window.innerHeight * DPR));
  const nodes = Array.from({ length: 80 }, () => ({
    x: Math.random() * W,
    y: Math.random() * H,
    vx: (Math.random() - 0.5) * 0.5,
    vy: (Math.random() - 0.5) * 0.5,
  }));

  let running = true;

  function draw() {
    if (!running) return;
    ctx.clearRect(0, 0, W, H);
    // puntos
    ctx.fillStyle = "rgba(255,255,255,.7)";
    nodes.forEach((p) => {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 1.2 * DPR, 0, Math.PI * 2);
      ctx.fill();
    });
    // líneas cortas
    ctx.lineWidth = 0.6 * DPR;
    ctx.strokeStyle = "rgba(255,255,255,.18)";
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const d = Math.hypot(dx, dy);
        if (d < 150 * DPR) {
          ctx.globalAlpha = 1 - d / (150 * DPR);
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.stroke();
        }
      }
    }
    ctx.globalAlpha = 1;
    requestAnimationFrame(draw);
  }
  draw();

  const onResize = () => {
    DPR = Math.min(2, window.devicePixelRatio || 1);
    W = canvas.width = Math.floor(window.innerWidth * DPR);
    H = canvas.height = Math.floor(window.innerHeight * DPR);
  };
  window.addEventListener("resize", onResize);

  return () => {
    running = false;
    window.removeEventListener("resize", onResize);
    canvas.remove();
  };
}
