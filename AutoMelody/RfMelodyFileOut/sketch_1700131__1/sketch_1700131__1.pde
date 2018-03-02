 import themidibus.*; //Import the library

MidiBus myBus; // The MidiBus
String[] data_1ch;
int[] firstch_array;
String[] data_2ch;
int[] secondch_array;
String[] data_10_1ch;
int[] Dr_ba_ch_array;
String[] data_10_2ch;
int[] Dr_rcy_ch_array;

int Current_Note_1ch = 0;
int Current_Note_2ch = 0;
int Current_Note_10_1ch = 0;
int Current_Note_10_2ch = 0;
 
 float[] tde_array;
 float[][] rythm_value_array;
 float[][] pitch_value_array;
 float[] note_weight_array;
 int i = 0;
 int melody_length = 0;
 String[] data;
 String[]data_rythm;
 String[]data_pitch;
 int SamplingRate = 32;
 int frame =80;
 color bg = (#fef0cb);
 color dark = (#fc5b86);
 color light = (#fdd35c);
 color text_col = (#2d3c80);
 color text_col1 = (#52802d);
 color text_col2 = (#52802d);
 color text_col3 = (#52802d);
 
void setup() {      
  size(1200, 400);
  frameRate(13);
  
  data = loadStrings("test.csv");
  melody_length = data.length;
  tde_array = new float[melody_length];
  for(int tmp = 0; tmp < melody_length ; tmp++){  
    String[] row_data = data[tmp].split(",",-1);
    tde_array[tmp] = float( row_data[0] ) * 100;
  }
  data_rythm = loadStrings("test_rythm.csv");
  rythm_value_array = new float[melody_length][SamplingRate];
  for(int row = 0; row < melody_length ; row++){  
    String[] row_data = data_rythm[row].split(",",-1);
    for(int col = 0; col < SamplingRate; col++){
      rythm_value_array[row][col] = float( row_data[col] ) * 200;
    }
  }
  data_pitch = loadStrings("test_pitch.csv");
  pitch_value_array = new float[melody_length][12];
  for(int row = 0; row < melody_length ; row++){  
    String[] row_data = data_rythm[row].split(",",-1);
    for(int col = 0; col < 12; col++){
      pitch_value_array[row][col] = float( row_data[col] ) * 200;
    }
  }
  
  //myBus = new MidiBus(this, -1, "Microsoft GS Wavetable Synth");
   myBus = new MidiBus(this, -1, "microX 1 SOUND");

  //myBus = new MidiBus(this, -1, "Java Sound Synthesizer");
  
  data_1ch = loadStrings("test_ch1.csv");
  //int melody_length = data_1ch.length;
  firstch_array = new int[melody_length];
  for(int tmp = 0; tmp < melody_length ; tmp++){  
  String[] row_data = data_1ch[tmp].split(",",-1);
  firstch_array[tmp] = int( row_data[0] );
  }
  
  data_2ch = loadStrings("test_ch2.csv");
  //int melody_length = data_1ch.length;
  secondch_array = new int[melody_length];
  for(int tmp = 0; tmp < melody_length ; tmp++){  
  String[] row_data = data_2ch[tmp].split(",",-1);
  secondch_array[tmp] = int( row_data[0] );
  }
  
  data_10_1ch = loadStrings("test_ch10_1.csv");
  // int melody_length = data_10_1ch.length;
  Dr_ba_ch_array = new int[melody_length];
  for(int tmp = 0; tmp < melody_length ; tmp++){  
  String[] row_data = data_10_1ch[tmp].split(",",-1);
  Dr_ba_ch_array[tmp] = int( row_data[0] );
  }
  
  data_10_2ch = loadStrings("test_ch10_2.csv");
  int melody_length = data_10_1ch.length;
  Dr_rcy_ch_array = new int[melody_length];
  for(int tmp = 0; tmp < melody_length ; tmp++){  
  String[] row_data = data_10_2ch[tmp].split(",",-1);
  Dr_rcy_ch_array[tmp] = int( row_data[0] );
  }
  
  
}

void draw() {
    int O_of_5_x = 110;
    int O_of_5_y = 200;
    int rythm_x = 360;
    int rythm_y = 200;
    int tde_x_x = 1200;
    int tde_x_y = 200;
    int tde_y_x = 530;
    int tde_y_y = 100;
    
    float Weight_C = pitch_value_array[i][0];
    float Weight_Db = pitch_value_array[i][1];
    float Weight_D = pitch_value_array[i][2];
    float Weight_Eb =pitch_value_array[i][3];
    float Weight_E = pitch_value_array[i][4];   
    float Weight_F = pitch_value_array[i][5];
    float Weight_Gb = pitch_value_array[i][6];
    float Weight_G = pitch_value_array[i][7];
    float Weight_Ab = pitch_value_array[i][8];   
    float Weight_A = pitch_value_array[i][9];
    float Weight_Bb = pitch_value_array[i][10];
    float Weight_B = pitch_value_array[i][11];
    
    background( bg );
    
    if(i == 0){
        
    }
    
    strokeWeight( 1 );
    stroke( light );
    fill( light );
    arc( O_of_5_x, O_of_5_y, Weight_C, Weight_C, PI*3/6, PI*4/6 );
    arc( O_of_5_x, O_of_5_y, Weight_F, Weight_F, PI*4/6, PI*5/6 );
    arc( O_of_5_x, O_of_5_y, Weight_Bb, Weight_Bb, PI*5/6, PI*6/6 );
    arc( O_of_5_x, O_of_5_y, Weight_Eb, Weight_Eb, PI*6/6, PI*7/6 );
    arc( O_of_5_x, O_of_5_y, Weight_Ab, Weight_Ab, PI*7/6, PI*8/6 );
    arc( O_of_5_x, O_of_5_y, Weight_Db, Weight_Db, PI*8/6, PI*9/6 );    
    arc( O_of_5_x, O_of_5_y, Weight_Gb, Weight_Gb, PI*9/6, PI*10/6 );
    arc( O_of_5_x, O_of_5_y, Weight_B, Weight_B, PI*10/6, PI*11/6 );
    arc( O_of_5_x, O_of_5_y, Weight_E, Weight_E, PI*11/6, PI*12/6 );
    arc( O_of_5_x, O_of_5_y, Weight_A, Weight_A, PI*0, PI*1/6 );
    arc( O_of_5_x, O_of_5_y, Weight_D, Weight_D, PI*1/6, PI*2/6 );
    arc( O_of_5_x, O_of_5_y, Weight_G, Weight_G, PI*2/6, PI*3/6 );
    fill( text_col1 );
    textSize(32);
    textAlign(CENTER);
    text("Pitch\nCircle of 5th",O_of_5_x,O_of_5_y + 100);
    
    float[] rythm_value_bar = rythm_value_bar(rythm_value_array,SamplingRate,i);
    int j = i % SamplingRate ;
    float l = rythm_value_bar[j] ;
    rythm_value(rythm_x, rythm_y, rythm_value_bar,light);   
    rythm_graph(i,SamplingRate,l,dark,rythm_x,rythm_y);
    fill( text_col2 );
    text("Rhythm\nOne musical bar",rythm_x,rythm_y + 100);    
    graph(TDE_graph(tde_array,i,frame),tde_x_x,tde_x_y,tde_y_x,tde_y_y,light,dark);
    textSize(32);
    textAlign(CENTER);
    fill( text_col3 );
    text("Reward prediction error",(tde_x_x+tde_y_x)/2,tde_x_y + 100);
    
    Current_Note_1ch = Convert_midi(firstch_array,i,1,11,Current_Note_1ch,100);
    Current_Note_2ch = Convert_midi(secondch_array,i,1,14,Current_Note_2ch,58);
    Current_Note_10_1ch = Convert_midi_dr(Dr_ba_ch_array,i,80,Current_Note_10_1ch);
    Current_Note_10_2ch = Convert_midi_dr(Dr_rcy_ch_array,i,37,Current_Note_10_2ch);
    
    fill( text_col );
    textSize(40);
    textAlign(CENTER);
    text("Actor Critic Melody",600,60);
    i ++ ;
    if(i > melody_length-1){
      myBus.sendNoteOff(1, Current_Note_1ch, 100); 
      myBus.sendNoteOff(2, Current_Note_2ch, 100); 
      noLoop();
    }
    
 
}

void rythm_graph( int t, int SR, float l, color col, int rythm_x, int rythm_y ) {
    strokeWeight( 1 );
    stroke( col );
    fill( col);
    float tmp_s = PI * 2 * i / SR + PI * 3/2;
    float tmp_d = PI * 2 * 1 / SR ;
    float start = tmp_s;
    float end = tmp_s + tmp_d;
    arc( rythm_x, rythm_y, l, l, start , end);
}

void rythm_value(int rythm_x, int rythm_y, float l[],color col){
     strokeWeight( 1 );
     stroke( col );
     fill( col );
     int st = l.length;
     for (int tmp = 0; tmp < l.length; tmp++){
       float tmp_s = PI * 2 * tmp / st + PI * 3/2;
       float tmp_d = PI * 2 * 1 / st ;
       float start = tmp_s;
       float end = tmp_s + tmp_d;
       arc( rythm_x, rythm_y, l[tmp], l[tmp], start, end);
     }
}

float[] rythm_value_bar(float d_array[][],int sr, int i){
    float[] bar = new float[sr];
    for(int tmp = 0; tmp < sr; tmp++){
        bar[tmp] = d_array[i][tmp];
    }
    return bar;
}

void graph(ArrayList<Float> tde, int x_x, int x_y, int y_x, int y_y, color col_p, color col_m){
    int width = x_x - y_x;
    int frame = tde.size();
    for (int t = 0; t < frame; t++){
      float x = t * (width / frame) + y_x;
      float y = x_y - tde.get(t);
      strokeWeight(3.8);
      if ( tde.get(t) < 0 ){
        stroke( col_m );
      }else{
        stroke(col_p );
      }
      point(x, y);
     }
}

ArrayList<Float> TDE_graph(float tde[], int i, int frame){
     ArrayList<Float> window;
     window = new ArrayList<Float>();
     if ( i < frame ){
         for (int tmp = 0; tmp < i + 1 ; tmp++){
           window.add(tde[tmp]) ;
         }
      }else{
         int tmp = i - frame + 1;
         for (int tmp2 = 0; tmp2 < frame; tmp2++){
           window.add(tde[tmp]) ;
           tmp ++;
         }
      }
      return window;
}


int Convert_midi(int note_array[],int i, int ch, int inst, int Curent_Note, int velo){
  int note = note_array[i] ;
  if( note > 0 ){
  byte inst_data[] = new byte[2];
       inst_data[0] = byte(0xC0 + ch);
       inst_data[1] = byte(inst);
    myBus.sendMessage(inst_data);
    myBus.sendNoteOff(ch, Curent_Note, velo); // Send a Midi nodeOff
    Curent_Note = note_array[i];
    myBus.sendNoteOn(ch, note_array[i], velo); // Send a Midi noteOn
  }else{
  }
  return Curent_Note;
}

int Convert_midi_dr(int note_array[],int i, int inst, int Curent_Note){
  int note = note_array[i] ;
  if( note > 0 ){
  byte inst_data[] = new byte[2];
       inst_data[0] = byte(0xC9);
       inst_data[1] = byte(inst);
    myBus.sendMessage(inst_data);
    Curent_Note = inst;
    myBus.sendNoteOn(9, inst, 40); // Send a Midi noteOn
  }else{
  }
  return inst;
}