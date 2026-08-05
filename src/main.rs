#[macro_use] extern crate rocket;
use rocket::{Build, Rocket};

#[launch]
fn rocket() -> Rocket<Build>{
    wikify::PAGE_PROVIDERS
        .set(Mutex::new(Vec::new()))
        .expect("Failed to initialize PAGE_PROVIDERS");
    rocket::build()
        .mount("/wiki", routes![wikify::wiki])
        .mount("/wiki", routes![wikify::wiki_post])
}
