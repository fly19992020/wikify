use rocket::http::ContentType;
use rocket::{get, post, response, Request, Response};
use std::collections::HashMap;
use std::io::Cursor;
use std::option;
use std::process::exit;
use std::sync::{Mutex, OnceLock};

pub type PostInfo = option::Option<String>;
pub type PageProvider = fn(&str, PostInfo) -> Result<String, u16>;
pub static PAGE_PROVIDERS: OnceLock<Mutex<HashMap<String, PageProvider>>> = OnceLock::new();

// Handle GET requests to /wiki/<name>
#[get("/<name>")]
pub fn wiki<'r>(name: &str) -> WikiPage {
    if name == "shut" {
        exit(0);
    } else {
        WikiPage::new(String::from(name), PostInfo::None)
    }
}

// Handle POST requests to /wiki/<name>
#[post("/<name>", data = "<data>")]
pub fn wiki_post<'r>(name: &str, data: PostInfo) -> WikiPage {
    WikiPage::new(String::from(name), data)
}

// A struct to represent a wiki page
pub struct WikiPage {
    namespace: String,
    page_name: String,
    page_path: String,
    post_data: PostInfo,
}

// Implement Responder for WikiPage to convert it into an HTTP response
impl<'r> response::Responder<'r, 'static> for WikiPage {
    fn respond_to(self, request: &'r Request<'_>) -> response::Result<'static> {
        match self.get_content() { // Get the content of the wiki page
            Ok(content) => Response::build()
                .header(ContentType::HTML)
                .sized_body(content.len(), Cursor::new(content))
                .ok(),
            Err(code) => Response::build().status(rocket::http::Status::new(code)).ok(),
        }
    }
}

impl WikiPage {
    // Create a new WikiPage instance
    pub fn new(name: String, post_data: PostInfo) -> WikiPage {
        WikiPage {
            namespace: "".to_string(),
            page_name: name,
            page_path: "./wiki".to_string(),
            post_data: post_data,
        }
    }

    // Get the content of the wiki page
    fn get_content(&self) -> Result<String, u16> {
        let file_name = format!("{}/{}", &self.page_path, &self.page_name); // get the file name from the uri
        let file_path = std::path::Path::new(file_name.as_str());
        if !file_path.exists() {
            return Err(404);
        }
        Ok(std::fs::read_to_string(file_name).unwrap())
    }
}
