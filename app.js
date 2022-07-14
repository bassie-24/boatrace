const express = require('express');
const { Client } = require(`pg`);
const app = express();
const basicAuth = require('basic-auth-connect');
var { PythonShell } = require('python-shell');

var username = process.env.BASIC_AUTH_USERNAME;
var password = process.env.BASIC_AUTH_PASSWORD;

if (username && password) {
  app.use(basicAuth(username, password));
}

app.use(express.static('public'));
app.use(express.urlencoded({extended: false}));

// ローカルで試すときに使う

const client = new Client({
  host:`localhost`,
  user:`manbou`,
  password:`nagasaki`,
  database:`task_list`,
  port: 5432
});




// heroku上で試すときに使う
/*
if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config();
  env_ssl = false
} else {
  env_ssl = {
    sslmode: 'require',
    rejectUnauthorized: false
  }
}
const client = new Client({
  host: process.env.ENV_HOST,
  user: process.env.ENV_USER,
  password: process.env.ENV_PASS,
  database: process.env.ENV_DB,
  port: 5432,
  ssl: env_ssl
});
*/

client.connect((err) => {
  if (err) {
    console.log('error connecting: ' + err.stack);
    return;
  }
  console.log('success');
});

app.get('/', (req, res) => {
  res.render('test.ejs');
});

app.post('/echo', (req, res) => {
  var options = {
    pythonPath: './general/Scripts/python',
    // pythonPath: 'C:/Users/ryooo/anaconda3/envs/general/python',
    scriptPath: './python_code/'
  }
  var pyshell = new PythonShell('predict.py', options);
  pyshell.send(req.body.itemName[0]);
  pyshell.send(req.body.itemName[1]);
  pyshell.send(req.body.itemName[2]);
  pyshell.send(req.body.itemName[3]);
  //   /* ------------------------------
  // 表示用の関数
  // ------------------------------ */
  // let dispLoading = (msg) => {
  //   // 引数なしの場合、メッセージは非表示。
  //   if(msg === undefined ) msg = "";
    
  //   // 画面表示メッセージを埋め込み
  //   var innerMsg = "<div id='innerMsg'>" + msg + "</div>";  
    
  //   // ローディング画像が非表示かどうかチェックし、非表示の場合のみ出力。
  //   if($("#nowLoading").length == 0){
  //     $("body").append("<div id='nowLoading'>" + innerMsg + "</div>");
  //   }
  // }
  
  // /* ------------------------------
  // 表示ストップ用の関数
  // ------------------------------ */
  // let removeLoading = () => {
  //   $("#nowLoading").remove();
  // }  

  let f1 = () => {
    return new Promise((resolve, reject) => {
      var array = [];
      pyshell.on('message', data => {
        console.log(data);
        array.push(data);
        // output = data;
        // console.log('aaa');
        // console.log(output);
        // setTimeout(() => {
        //   resolve('aaa');
        // }, 1000);
        resolve(array);
      });
    });
  }

  // Loading 画像を表示
  // dispLoading("処理中...");
  f1().then(result => {
    console.log('aaa');
    console.log(result);
    // Loading 画像を消す
    // removeLoading();
    res.render('test2.ejs', {predicts:result});
  });
  
});

app.get('/index', (req, res) => {
  client.query(
  'select * from items',
  (error,results) => {
    console.log(results.rows);
    res.render('index.ejs',{items:results.rows});
  });
}); 

app.get('/new', (req, res) => {
  res.render('new.ejs');
});

app.get('/completed', (req, res) => {
  client.query(
  'select * from completed_items',
  (error,results)=>{
  console.log(results.rows);
  res.render('completed.ejs',{items:results.rows});
  });
});


app.post('/create', (req, res) => {
  client.query(
    'INSERT INTO items (name) VALUES ($1)',
    [req.body.itemName],
    (error, results) => {
      res.redirect('/index');
    }
  );
});

app.post('/delete/:id', (req, res) => {
  client.query(
    'DELETE FROM items WHERE id = $1',
    [req.params.id],
    (error, results) => {
      res.redirect('/index');
    }
  );
});

app.get('/edit/:id', (req, res) => {
  
  client.query(
    'SELECT * FROM items WHERE id = $1',
    [req.params.id],
    (error, results) => {
      res.render('edit.ejs', {item: results.rows[0]});
    }
  );
});

app.post('/update/:id', (req, res) => {
  client.query(
    'UPDATE items SET name = $1 WHERE id = $2',
    [req.body.itemName, req.params.id],
    (error, results) => {
      res.redirect('/index');
    }
  );
});

app.post('/complete/:id', (req, res) => {
  client.query(
    'SELECT * FROM items WHERE id = $1',
    [req.params.id],
    (error, results) => {
      const completed_name = results.rows[0].name;
      client.query(
        'DELETE FROM items WHERE id = $1',
        [req.params.id],
        (error, results) => {}
      );
    
      client.query(
        'INSERT INTO completed_items (name) VALUES ($1)',
        [completed_name],
        (error, results) => {
          console.log(completed_name);
          res.redirect('/index');
        }
      );
    }
  );

  
});

app.listen(process.env.PORT || 5000);
// app.listen(3000);