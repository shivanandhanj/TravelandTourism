
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import Register from './components/regsiter';
import Header from './components/header';
import Footer from './components/Footer';
import Login  from './components/Login';
import { UserProvider } from './components/UserContext';
import AdminPage from './components/AdminPage';
import UserPage from './components/UserPage';
import AddPage  from './components/AddPage';
import UserList from './components/UserList';
import Manager from './components/Manager';
import Contact from './components/Contact'
function App() {
  return (
    <UserProvider>
    <div className="">
     <Router>
        <Header />
        <Routes>
          {/* <Route path="/login" element={<Login />} /> */}
          <Route path="/register" element={<Register />} />
        
          <Route path="/login" element={<Login />} />
          {/* <Route path="/admin" element={<AdminPage />} /> */}
          <Route path="/user" element={<UserPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/" element={<UserList />} />
          <Route path="/manager" element={<Manager />} />
          <Route path="/contact" element={<Contact />} />

          
          {/* <Route path="/" element={<LandingPage />} /> */}
          {/* <Route path="/destin" element={<Destin />} /> */}
          {/* <Route path="/explore" element={<Explore />}  /> */}
          {/* <Route path="/contact" element={<Contact />}  /> */}
          
          
        </Routes>
        <Footer />
      </Router>
    </div>
    </UserProvider>
  );
}

export default App;
