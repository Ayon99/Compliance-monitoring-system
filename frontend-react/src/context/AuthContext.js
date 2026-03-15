import { createContext, useContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [token, setToken] = useState(null);
    const [user, setUser] = useState(null);

  useEffect(() => {
  const storedToken = localStorage.getItem("token");
  if (storedToken) {
    setToken(storedToken);
    const decoded = jwtDecode(storedToken);
    setUser(decoded);
  }
}, []);

  const login = (newToken) => {
  localStorage.setItem("token", newToken);
  setToken(newToken);
  const decoded = jwtDecode(newToken);
  setUser(decoded);
};

  const logout = () => {
  localStorage.removeItem("token");
  setToken(null);
  setUser(null);
};

  return (
    <AuthContext.Provider value={{ token, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}