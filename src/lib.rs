use rocket::http::ContentType;
use rocket::{get, post, response, Request, Response};
use std::io::Cursor;
use std::option;
use std::process::exit;

type PostInfo = option::Option<String>;

#[get("/<name>")]
pub fn wiki<'r>(name: &str) -> WikiPage {
    if name == "shut" {
        exit(0);
    } else {
        WikiPage::new(String::from(name), PostInfo::None)
    }
}

#[post("/<name>", data = "<data>")]
pub fn wiki_post<'r>(name: &str, data: PostInfo) -> WikiPage {
    WikiPage::new(String::from(name), data)
}

pub struct WikiPage {
    namespace: String,
    page_name: String,
    page_path: String,
    post_data: PostInfo,
}

impl<'r> response::Responder<'r, 'static> for WikiPage {
    fn respond_to(self, request: &'r Request<'_>) -> response::Result<'static> {
        match self.get_content() {
            Ok(content) => Response::build()
                .header(ContentType::HTML)
                .sized_body(content.len(), Cursor::new(content))
                .ok(),
            Err(code) => Response::build().status(rocket::http::Status::new(code)).ok(),
        }
    }
}

impl WikiPage {
    pub fn new(name: String, post_data: PostInfo) -> WikiPage {
        WikiPage {
            namespace: "".to_string(),
            page_name: name,
            page_path: "./wiki".to_string(),
            post_data: post_data,
        }
    }

    fn get_content(&self) -> Result<String, u16> {
        let file_name = format!("{}/{}", &self.page_path, &self.page_name); // get the file name from the uri
        let file_path = std::path::Path::new(file_name.as_str());
        if !file_path.exists() {
            return Err(404);
        }
        Ok(std::fs::read_to_string(file_name).unwrap())
    }
}
