from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'neu_quan_ly_de_cuong'


def get_db_connection():
    # Trỏ đúng vào file db cậu vừa tạo thành công
    conn = sqlite3.connect('db/PQHCHP.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Trên form HTML tên ô nhập vẫn là username, nhưng ta sẽ map nó với cột EMAIL trong DB
        email_input = request.form['username']
        password_input = request.form['password']

        conn = get_db_connection()
        # Chọc vào bảng CANBO (Cán bộ) của thầy để tìm User
        user = conn.execute('SELECT * FROM CANBO WHERE EMAIL = ? AND PASSWORD = ?',
                            (email_input, password_input)).fetchone()
        conn.close()

        if user:
            # Lưu thông tin phiên đăng nhập dựa trên các cột mới của thầy
            session['user_id'] = user['MACB']
            session['username'] = user['EMAIL']
            session['full_name'] = user['TENCB']
            session['role'] = user['ROLE']  # 'giangvien', 'admin_khoa', 'admin_hethong'
            return redirect(url_for('dashboard'))
        else:
            flash('Sai email hoặc mật khẩu!')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    # Lấy danh sách giảng viên để hiển thị tạm trên Dashboard của Admin
    users_list = conn.execute('SELECT * FROM CANBO WHERE ROLE = "giangvien"').fetchall()
    conn.close()

    return render_template('dashboard.html', users_list=users_list)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)