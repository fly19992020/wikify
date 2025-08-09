pub mod wikify {
    use rocket::http::ContentType;
    use rocket::{response, Request, Response};
    use std::io::Cursor;

    pub struct Page {
        namespace: String,
        page_name: String,
        page_path: String,
    }

    impl<'r> response::Responder<'r, 'static> for Page {
        fn respond_to(self, request: &'r Request<'_>) -> response::Result<'static> {
            let file_name = format!("{}/{}", &self.page_path, &self.page_name); // get the file name from the uri
            let file_path = std::path::Path::new(file_name.as_str());
            if !file_path.exists() {
                Err(rocket::http::Status { code: 404 })
            } else {
                let content = std::fs::read_to_string(file_name).unwrap();
                Response::build()
                    .header(ContentType::HTML)
                    .sized_body(content.len(), Cursor::new(content))
                    .ok()
            }
        }
    }

    impl Page {
        pub fn new(name: String) -> Page {
            Page {
                namespace: "".to_string(),
                page_name: name,
                page_path: "./wiki".to_string(),
            }
        }
    }
}
