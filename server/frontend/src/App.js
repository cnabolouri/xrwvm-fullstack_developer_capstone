import LoginPanel from "./components/Login/Login"
import { Routes, Route } from "react-router-dom";
import Register from "./components/Register/Register";   // <-- create this file
import Dealers from './components/Dealers/Dealers';
import Dealer from "./components/Dealers/Dealer";
import PostReview from "./components/Dealers/PostReview";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealers/>} />  
      <Route path="/dealer/:id" element={<Dealer/>} />
      <Route path="/postreview/:id" element={<PostReview/>} />
      {/* <Route path="/dealers" element={<Dealers />} />
      <Route path="/dealer/:id/*" element={<Dealer />} />
      <Route path="/postreview/:id/*" element={<PostReview />} /> */}
    </Routes>
  );
}
export default App;



// Good: allow trailing slash (and anything after) with /*
// so /dealer/4 and /dealer/4/ both match.

