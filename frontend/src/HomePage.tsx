import { useEffect, useState } from "react";
import "./HomePage.css";

function HomePage() {
  return (
    <>
      <Banner />
      <div className="main-view">
        <Sidebar />
        <Content />
      </div>
    </>
  );
}

function Banner() {
  return (
    <div className="banner">
      <h1>Secure View</h1>
    </div>
  );
}

function Sidebar() {
  return (
    <div className="sidebar">
      <h3>Página principal</h3>
      <h3>Cámaras</h3>
      <h3>Almacenamiento</h3>
      <h3>Notificariones</h3>
      <h3>Ajustes</h3>
    </div>
  );
}

function Content() {
  return (
    <div className="content">
      <TimeDisplay />
      <Notifications />
      <Video />
    </div>
  );
}

function TimeDisplay() {
  const [time, setTime] = useState<String>(new Date().toLocaleString());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date().toLocaleString());
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <div>
      <h2>Hora actual: {time}</h2>
    </div>
  );
}

function Notifications() {
  return (
    <div className="notifications">
      <h2>Últimas notificaciones</h2>
    </div>
  );
}

function Video() {
  return (
    <div>
      <h2>Cámaras principales</h2>
    </div>
  );
}

export default HomePage;
