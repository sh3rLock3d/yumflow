import React, { useContext } from "react";
import { Context } from "../../Store";
import MyNeuralNetwork from "../common/MyNeuralNetwork";

function Homepage() {
  const [state, dispatch] = useContext(Context);
  console.log(state);

  return (
    <>
      <MyNeuralNetwork/>
      <div className="container-fluid">


        <div class="container p-4">
          <div class="row">
            <p>
              این وبسایت ابزاریست برای ساخت و مقایسه ی مدل های یادگیری ماشین با ابزار های شیوه ها و متد های مختلف، که اموزش و تست و پیشبینی بر روی داده ها را ساده تر میکند.
            </p>

          </div>
        </div>


        <footer class="bg-light text-center" id="footer">
          <div class="container p-4">
            <div class="row">

              <h5 class="text-uppercase">یادگیری چرخه ی ماشین</h5>

              <p>
                آزمایشگاه دکتر جعفری سیاوشانی<br />
                پروژه ی کارشناسی علی پورقاسمی<br/>
                دانشکده ی علوم و مهندسی کامپیوتر<br />
                دانشگاه صنعتی شریف<br />
                تهران، ایران<br />
              </p>

            </div>
          </div>

          <div class="text-center p-3" style={{ backgroundColor: '#00000033' }}>
            © 2022 Copyright:
            <a class="text-dark" href="https://mahdi.jafari.siavoshani.ir/">mahdi.jafari.siavoshani.ir</a>
          </div>

        </footer>
      </div>

    </>
  );
}

export default Homepage;
