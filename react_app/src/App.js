import './App.css';
import {Header} from './containers'
import { CTA, Navbar } from './components'
import {Login} from "./Api"

const App = () => {
  return (
    <div className="App">
      <div>
          <Navbar />       
          <Header />
      </div>
      <Login />
      <CTA />
    </div>
  );
}

export default App;
