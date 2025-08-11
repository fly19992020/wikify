#[macro_use] extern crate rocket;
use rocket::{Build, Rocket};

#[launch]
fn rocket() -> Rocket<Build>{
    rocket::build()
        .mount("/wiki", routes![wikify::wiki])
        .mount("/wiki", routes![wikify::wiki_post])
}
