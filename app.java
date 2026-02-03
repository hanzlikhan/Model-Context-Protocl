package com.example.myapplication
public class Click extends AppCompatActivity {
    Button btnno1;
    protected void onCreate(Bundle savedInstanceState) {
        setContentView(R.layout.activity_click);
        btnno1 = findViewById(R.id.button_send1);
        android:id="@+id/button_send1"
        btnno1.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(click.this, Signin.class);
                startActivity(intent);
            )}};
