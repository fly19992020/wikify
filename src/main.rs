#[macro_use] extern crate rocket;

use std::fs;
use rocket::response::content::RawHtml;

#[get("/<name>")]
fn hello<'r>(name: &str) -> Option<RawHtml<String>> {
    if name == "Main.html" {
        let path = "./src/Main_Page.html";
        Some(RawHtml(fs::read_to_string(path).unwrap()))
    }
    else {
        Some(RawHtml(String::new()))
    }
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![hello])
}