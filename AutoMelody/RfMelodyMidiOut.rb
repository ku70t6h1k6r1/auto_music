require 'unimidi'
#for midi
class Convert_Note_midi
	def initialize(a_pre,a)
		@a_pre = a_pre
		@a = a
		#@twelve_notes_midi = {"C" => 48,"Db" => 49,"D" => 50,"Eb" => 51,"E" => 52 ,"F" => 53 ,"Gb" => 54 , "G" => 55 , "Ab" => 56 ,"A" => 57 ,"Bb" => 58 ,"B" => 59}
		#@twelve_notes_midi = {"C" => 60,"Db" => 61,"D" => 62,"Eb" => 63,"E" => 64 ,"F" => 65 ,"Gb" => 66 , "G" => 67 , "Ab" => 68 ,"A" => 69 ,"Bb" => 70 ,"B" => 71}
		@twelve_notes_midi = {"C" => 72,"Db" => 73,"D" => 74,"Eb" => 75,"E" => 76 ,"F" => 77 ,"Gb" => 78 , "G" => 79 , "Ab" => 80 ,"A" => 81 ,"Bb" => 82 ,"B" => 83}
		@a_post = @twelve_notes_midi[@a]
		if (@a_post - @a_pre) > 5 then
			@a_post = @a_post - 12
		elsif (@a_post - @a_pre) < -6 then
			@a_post = @a_post + 12
		else
			@a_post = @a_post
		end
	end
	def output
		@a_post
	end
end

class Convert_Note_midi_Bass
	def initialize(a_pre,a)
		@a_pre = a_pre
		@a = a
		@twelve_notes_midi = {"C" => 48,"Db" => 49,"D" => 50,"Eb" => 51,"E" => 52 ,"F" => 53 ,"Gb" => 54 , "G" => 55 , "Ab" => 56 ,"A" => 57 ,"Bb" => 58 ,"B" => 59}
		#@twelve_notes_midi = {"C" => 60,"Db" => 61,"D" => 62,"Eb" => 63,"E" => 64 ,"F" => 65 ,"Gb" => 66 , "G" => 67 , "Ab" => 68 ,"A" => 69 ,"Bb" => 70 ,"B" => 71}
		#@twelve_notes_midi = {"C" => 72,"Db" => 73,"D" => 74,"Eb" => 75,"E" => 76 ,"F" => 77 ,"Gb" => 78 , "G" => 79 , "Ab" => 80 ,"A" => 81 ,"Bb" => 82 ,"B" => 83}
		@a_post = @twelve_notes_midi[@a]
		if (@a_post - @a_pre) > 5 then
			@a_post = @a_post - 12
		elsif (@a_post - @a_pre) < -6 then
			@a_post = @a_post + 12
		else
			@a_post = @a_post
		end
	end
	def output
		@a_post
	end
end

class Bpm
	def initialize(bpm,sr)
		@sr = sr.to_f
		@output = (60.0/bpm) * 4 / @sr
	end
	def output
		@output
	end
end
#Note

class Situation
	def initialize(notes)
		@twelve_notes = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
		@size = notes.size
		@output = Hash.new()
		@twelve_notes.each do |note|
			@output[note]= notes.select{|n|n == note}.size/@size.to_f
		end
	end
	def output
		@output
	end
end

class Weight
	def initialize(w,note,a,d)
		@w = w
		@note = note
		@a = a.to_f
		@d = d.to_f
		@w[note] = @w[@note].to_f + @a * @d 
	end
	def output
		@w
	end
end

class Qvalue
	def initialize(s,w)
		@twelve_notes = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
		@s = s
		@w = w
		@output = Hash.new()
		@twelve_notes.each do |note|
			@output[note]= @s[note] * @w[note]
		end
	end
	def output
		@output
	end
end

class Policy
	def initialize(q,temp)
		@twelve_notes = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
		@q = q
		@b = 1/temp.to_f
		@p_num = Hash.new
		@p_den = 0
		@p = Hash.new
		@twelve_notes.each do |note|
			@p_den = @p_den + Math.exp(@b * @q[note])
			@p_num[note] = Math.exp(@b * @q[note])
		end
		@twelve_notes.each do |note|
			@p[note] = @p_num[note] / @p_den
		end
	end
	def output
		@p
	end
end

class Dice
	def initialize(p)
		@twelve_notes = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
		@p = p
		@tmp = 0.to_f
		@random = Random.new.rand(1e8)/1e8.to_f
		@twelve_notes.each do |note|
			@tmp = @tmp + @p[note]
			if @tmp > @random then
				@note = note
				break
			end
		end
	end
	def output
		@note
	end
end

class Tderror
	def initialize(a,s,w,t,tv)
		@twelve_notes = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
		@a = a 
		@s = s
		@w = w
		@r = 0
		@er = 0
		@tv = tv
		@temp = t
		@q = Qvalue.new(@s,@w).output
		@p = Policy.new(@q,@temp).output
		@twelve_notes.each do |note|
			@r = @r + @tv[note][@a].to_f * @s[note].to_f
		end
		@twelve_notes.each do |note_c|	
			@twelve_notes.each do |note_r|
				@er = @er + @tv[note_r][note_c].to_f * @s[note_r].to_f * @p[note_c].to_f
			end
		end
		@output = @r - @er 
	end
	def output
		@output
	end
end

class Tonalvalue
	def initialize(v)
		@twelve_notes = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
		@v = v + v
		@output = Hash.new{|h,k| h[k] = {} }
		@j = 0
		@i_size = @twelve_notes.size
		@twelve_notes.each do |note_r|
			@i = @i_size + @j
			@twelve_notes.each do |note_c|
				@output[note_r][note_c] = @v[@i]
				@i = @i + 1
			end
			@j = @j - 1
		end
	end
	def output
		@output
	end
end

#beat
class Wave
	def initialize(hz,sr)
		@Hz = hz
		@sr = sr
		@t = 0
		@pi = Math::PI.to_f
		@output = []
		@sr.times do
			@output.push(((1 + Math.cos(@pi*2*@Hz*@t/@sr))/@sr).to_f)
			@t = @t + 1
		end
	end
	def output
		@output
	end
end

class Sumwave
	def initialize(v,sr)
		@v = v
		@sr = sr
		@beat = v.size
		@v_std = []
		@w_sum = Array.new(@sr){0}
		@sum = 0
		@i = 1
		@v.each do |f|
			@sum = @sum + f 
		end
		@v.each do |f|
			@v_std.push(f.to_f/@sum)
		end
		@beat.times do
			@w = Wave.new(@i,@sr).output
			@t = 0
			@w.each do |p|
				@w_sum[@t] = @w_sum[@t] + @v_std[(@i-1)] * p
				@t = @t + 1
			end
			@i = @i + 1
		end
	end
	def output
		@w_sum
	end
end

class Sumwave_Value
	def initialize(prob,v)
		@prob = prob
		@v = v
		@output = []
		@w = (1 / ( 1 + Math.exp(@v) ) ).to_f
		@prob.each do |beat|
			@output.push(beat*@w)
		end
	end
	def output
		@output
	end
end

class Situation_tmp_beat
	def initialize(abeat,a,samplingtime)
		@abeat = abeat
		@a = a
		@st = samplingtime
		@abeat[@st] = @abeat[@st] + @a 
	end
	def output
		@abeat
	end
end

class Situation_tmp
	def initialize(abeat)
		@s = abeat
		@sum = 0
		@output = []
		@s.each do |beat|
			@sum = @sum + beat
		end
		@s.each do |beat|
			@output.push((beat.to_f/@sum)) 
		end
	end
	def output
		@output
	end
end

class Beat_parm
	def initialize(tde_sum)
		@e = tde_sum - 1
		@output = 32.0 / (1 + Math.exp(-3 * @e))
	end
	def output
		@output
	end
end

class Policy_beat
	def initialize(situation_tmp,prob,sr,beat_parm)
		@prob = prob
		@beat_parm = beat_parm
		@sr = sr
		@s = situation_tmp
		@i = 0
		@output =  []
		@prob.each do |beat|
			@output.push( beat.to_f * @sr.to_f * @s[@i] * @beat_parm)
			@i = @i + 1
		end
	end
	def output
		@output
	end
end

class Convert_Value
	def initialize(v,tderror)
		@v = v
		@tde = tderror
		@i = 1
		@g = 1 / ( 1 + Math.exp(@tde) )
		@output = []
		@v.each do |beat|
			tmp = beat * (@g ** @i)
			@output.push(tmp.to_f)
			@i = @i + 1
		end
	end
	def output
		@output
	end
end

class Dice_beat
	def initialize(policy,samplingtime)
		@p = policy
		@st = samplingtime
		@a = 0
		@random = Random.new.rand(1e12)/1e12.to_f
		if @p[@st] > @random then
			@a = 1
		end
	end
	def output
		@a
	end
end


#初期値note
@Note_array = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
@NoteValue_table = [1 , 0 , 1 , 0 ,1 , 0 , 0 , 1 , 0 , 0 , 0 , 0]
@TV = Tonalvalue.new(@NoteValue_table).output
@W = {"C" => 1,"Db" => 1,"D" => 1,"Eb" => 1,"E" => 1 ,"F" => 1 ,"Gb" => 1 , "G" => 1 , "Ab" => 1 ,"A" => 1 ,"Bb" => 1 ,"B" => 1}
@S = Situation.new(@Note_array).output
@temp = 3

#初期値beat
@SR = 32
@Beat_parm = 4.0#1小節の確率
#@V=[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
@V=[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

@Prob = Sumwave.new(@V,@SR).output
@Beat_array = Array.new(@SR){1}
@S_beat = Situation_tmp.new(@Beat_array).output
@Policy = Policy_beat.new(@S_beat,@Prob,@SR,@Beat_parm).output
@TDE_sum = 0
@r = 0.9
@LearningRate = 0.2

#midi
@Device = UniMIDI::Output.gets
@A_midi = 0
@A_bass_midi = 0
@Duration = Bpm.new(120.0,@SR).output


@i = 0
5000.times do
	@Samplingtime = 0
	@tmp = 0
	puts "###############"
	@SR.times do 
		@A_boolean = Dice_beat.new(@Policy, @Samplingtime).output
		
		@A_badrum_boolean = Dice_beat.new(@Policy, @Samplingtime).output
		if @A_badrum_boolean == 1 then
			@Device.puts(0xc9) # note on message
    		@Device.puts(0x99, 36, 40) # note on message
		end
		
		@A_rcymbal_boolean = Dice_beat.new(@Policy, @Samplingtime).output
		if @A_rcymbal_boolean == 1 then
			@Device.puts(0xc9) # note on message
    		@Device.puts(0x99, 51, 40) # note on message
		end
		
		# Note決定
		if @A_boolean == 1 then
			@Q = Qvalue.new(@S,@W).output
			@P = Policy.new(@Q,@temp).output
			@A = Dice.new(@P).output
			puts @A
			@Device.puts(0x80, @A_midi)
			@A_midi = Convert_Note_midi.new(@A_midi,@A).output
			@Device.puts(0xc0,11) # note on message
    		@Device.puts(0x90, @A_midi, 100) # note on message
			@Note_array.push(@A)
			@S = Situation.new(@Note_array).output
			@TDE = Tderror.new(@A,@S,@W,@temp,@TV).output
			@W = Weight.new(@W,@A,@LearningRate,@TDE).output
			@TDE_sum = @TDE + @r * @TDE_sum
			@Beat_parm = Beat_parm.new(@TDE_sum).output
		end
		# Note決定
		@A_bass_boolean = Dice_beat.new(@Policy, @Samplingtime).output
		if @A_bass_boolean == 1 then
			@Q = Qvalue.new(@S,@W).output
			@P = Policy.new(@Q,@temp).output
			@A_bass = Dice.new(@P).output
			@Device.puts(0x81, @A_bass_midi)
			@A_bass_midi = Convert_Note_midi_Bass.new(@A_bass_midi,@A_bass).output
			@Device.puts(0xc1,32) # note on message
    		@Device.puts(0x91, @A_bass_midi, 100) # note on message
			@Note_array.push(@A_bass_midi)
			@S = Situation.new(@Note_array).output
			@TDE = Tderror.new(@A_bass,@S,@W,@temp,@TV).output
			@W = Weight.new(@W,@A_bass,@LearningRate,@TDE).output
			@TDE_sum = @TDE + @r * @TDE_sum
			@Beat_parm = Beat_parm.new(@TDE_sum).output
		end
		# 状態更新
		@Post_V = Convert_Value.new(@V,@TDE_sum).output
		@Prob = Sumwave.new(@Post_V,@SR).output
		@Policy = Policy_beat.new(@S_beat,@Prob,@SR,@Beat_parm).output
		@Beat_array = Situation_tmp_beat.new(@Beat_array,@A_boolean,@Samplingtime).output
		@Samplingtime = @Samplingtime + 1
		sleep @Duration
	end
	@S_beat = Situation_tmp.new(@Beat_array).output
	@Policy = Policy_beat.new(@S_beat,@Prob,@SR,@Beat_parm).output
	@i = @i + 1
	puts @TDE
	puts @TDE_sum
end

