import { Route, Routes } from "react-router-dom";
import "./App.css";
import { Navbar } from "./components/Navbar";
import { Home, Signup, ProviderLogin, ProviderSignup, Main} from "./components/pages";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/doclogin" element={<ProviderLogin />} />
        <Route path="/docsign" element={<ProviderSignup />} />
        <Route path="/main" element={<Main />} />
      </Routes>
    </div>
  );
}

export default App;
