// import React, { useState, useEffect } from 'react';
// import { useParams } from 'react-router-dom';
// import "./Dealers.css";
// import "../assets/style.css";
// import Header from '../Header/Header';


// const PostReview = () => {
//   const [dealer, setDealer] = useState({});
//   const [review, setReview] = useState("");
//   const [model, setModel] = useState();
//   const [year, setYear] = useState("");
//   const [date, setDate] = useState("");
//   const [carmodels, setCarmodels] = useState([]);

//   let curr_url = window.location.href;
//   let root_url = curr_url.substring(0,curr_url.indexOf("postreview"));
//   let params = useParams();
//   let id =params.id;
//   let dealer_url = root_url+`djangoapp/dealer/${id}`;
//   let review_url = root_url+`djangoapp/add_review`;
//   let carmodels_url = root_url+`djangoapp/get_cars`;

//   const postreview = async ()=>{
//     let name = sessionStorage.getItem("firstname")+" "+sessionStorage.getItem("lastname");
//     //If the first and second name are stores as null, use the username
//     if(name.includes("null")) {
//       name = sessionStorage.getItem("username");
//     }
//     if(!model || review === "" || date === "" || year === "" || model === "") {
//       alert("All details are mandatory")
//       return;
//     }

//     let model_split = model.split(" ");
//     let make_chosen = model_split[0];
//     let model_chosen = model_split[1];

//     let jsoninput = JSON.stringify({
//       "name": name,
//       "dealership": id,
//       "review": review,
//       "purchase": true,
//       "purchase_date": date,
//       "car_make": make_chosen,
//       "car_model": model_chosen,
//       "car_year": year,
//     });

//     console.log(jsoninput);
//     const res = await fetch(review_url, {
//       method: "POST",
//       headers: {
//           "Content-Type": "application/json",
//       },
//       body: jsoninput,
//   });

//   const json = await res.json();
//   if (json.status === 200) {
//       window.location.href = window.location.origin+"/dealer/"+id;
//   }

//   }
//   const get_dealer = async ()=>{
//     const res = await fetch(dealer_url, {
//       method: "GET"
//     });
//     const retobj = await res.json();
    
//     if(retobj.status === 200) {
//       let dealerobjs = Array.from(retobj.dealer)
//       if(dealerobjs.length > 0)
//         setDealer(dealerobjs[0])
//     }
//   }

//   const get_cars = async ()=>{
//     const res = await fetch(carmodels_url, {
//       method: "GET"
//     });
//     const retobj = await res.json();
    
//     let carmodelsarr = Array.from(retobj.CarModels)
//     setCarmodels(carmodelsarr)
//   }
//   useEffect(() => {
//     get_dealer();
//     get_cars();
//   },[]);


//   return (
//     <div>
//       <Header/>
//       <div  style={{margin:"5%"}}>
//       <h1 style={{color:"darkblue"}}>{dealer.full_name}</h1>
//       <textarea id='review' cols='50' rows='7' onChange={(e) => setReview(e.target.value)}></textarea>
//       <div className='input_field'>
//       Purchase Date <input type="date" onChange={(e) => setDate(e.target.value)}/>
//       </div>
//       <div className='input_field'>
//       Car Make 
//       <select name="cars" id="cars" onChange={(e) => setModel(e.target.value)}>
//       <option value="" selected disabled hidden>Choose Car Make and Model</option>
//       {carmodels.map(carmodel => (
//           <option value={carmodel.CarMake+" "+carmodel.CarModel}>{carmodel.CarMake} {carmodel.CarModel}</option>
//       ))}
//       </select>        
//       </div >

//       <div className='input_field'>
//       Car Year <input type="int" onChange={(e) => setYear(e.target.value)} max={2023} min={2015}/>
//       </div>

//       <div>
//       <button className='postreview' onClick={postreview}>Post Review</button>
//       </div>
//     </div>
//     </div>
//   )
// }
// export default PostReview

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");          // will store JSON string: {"make":"...","model":"..."}
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const { id } = useParams();
  const root = `${window.location.origin}/`;

  const dealer_url    = `${root}djangoapp/dealer/${id}`;
  const review_url    = `${root}djangoapp/add_review`;
  const carmodels_url = `${root}djangoapp/get_cars`;

  const postreview = async () => {
    let name = (sessionStorage.getItem("firstname") || "") + " " + (sessionStorage.getItem("lastname") || "");
    if (name.trim() === "" || name.includes("null")) {
      name = sessionStorage.getItem("username") || "Anonymous";
    }
    if (!model || !review || !date || !year) {
      alert("All details are mandatory");
      return;
    }

    // model is a JSON string we stored in the option value
    const { make: make_chosen, model: model_chosen } = JSON.parse(model);

    const payload = {
      name,
      dealership: id,
      review,
      purchase: true,
      purchase_date: date,
      car_make: make_chosen,
      car_model: model_chosen,
      car_year: year,
    };

    const res = await fetch(review_url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const json = await res.json();
    if (json.status === 200) {
      window.location.href = `${window.location.origin}/dealer/${id}`;
    } else {
      alert("Posting review failed.");
      console.error("add_review response:", json);
    }
  };

  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url);
      const retobj = await res.json();
      if (retobj?.status === 200) {
        const d = Array.isArray(retobj.dealer) ? retobj.dealer[0] : retobj.dealer;
        if (d) setDealer(d);
      }
    } catch (e) {
      console.error("get_dealer error:", e);
    }
  };

  const get_cars = async () => {
    try {
      const res = await fetch(carmodels_url);
      const retobj = await res.json();
      // accept either CarModels or car_models
      const list = Array.isArray(retobj?.CarModels)
        ? retobj.CarModels
        : Array.isArray(retobj?.car_models)
          ? retobj.car_models
          : [];
      console.log("get_cars response:", retobj);   // <-- see what the backend returns
      setCarmodels(list);
    } catch (e) {
      console.error("get_cars error:", e);
      setCarmodels([]);
    }
  };

  useEffect(() => {
    get_dealer();
    get_cars();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  return (
    <div>
      <Header/>
      <div style={{margin:"5%"}}>
        <h1 style={{color:"darkblue"}}>{dealer?.full_name || "Dealer"}</h1>

        <textarea id='review' cols='50' rows='7'
          onChange={(e) => setReview(e.target.value)} />

        <div className='input_field'>
          Purchase Date{" "}
          <input type="date" onChange={(e) => setDate(e.target.value)} />
        </div>

        <div className='input_field'>
          Car Make / Model
          <select
            name="cars"
            id="cars"
            value={model}
            onChange={(e) => setModel(e.target.value)}
            defaultValue=""
          >
            <option value="" disabled hidden>Choose Car Make and Model</option>
            {carmodels.length === 0 ? (
              <option value="" disabled>No car models available</option>
            ) : (
              carmodels.map((cm, idx) => {
                // accept either key style
                const make  = cm.CarMake ?? cm.car_make ?? "";
                const mdl   = cm.CarModel ?? cm.car_model ?? "";
                return (
                  <option
                    key={`${make}-${mdl}-${idx}`}
                    value={JSON.stringify({ make, model: mdl })}
                  >
                    {make} {mdl}
                  </option>
                );
              })
            )}
          </select>
        </div>

        <div className='input_field'>
          Car Year{" "}
          <input
            type="number"
            onChange={(e) => setYear(e.target.value)}
            max={2025}
            min={2015}
          />
        </div>

        <div>
          <button className='postreview' onClick={postreview}>Post Review</button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;
