#[macro_use] extern crate rocket;

use std::process::exit;
use rocket::response::content::RawHtml;
use rocket::{Build, Rocket};

#[get("/<name>")]
fn wiki<'r>(name: &str) -> wikify::wikify::Page {
    if name == "shut" {
        exit(0);
    } else {
        wikify::wikify::Page::new(String::from(name))
    }
}

#[launch]
fn rocket() -> Rocket<Build>{
    rocket::build()
        .mount("/wiki", routes![wiki])
}
