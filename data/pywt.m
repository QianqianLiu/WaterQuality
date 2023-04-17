function output = pywt()
    % 约定从data_used_for_wavlet.csv中读取数据，第一列是要分解的数据，第二列是level
    text = textread('wavlet_type.txt', '%s');
    data = csvread('data_used_for_wavlet.csv');
    
    level = data(1, 2);
    data = data(:, 1);
    wavename = text{:};
 
    % 多尺度/级分解:wavedec
    [C,L]=wavedec(data, level, wavename);
    output_matrix = [];
    
    % 系数提取: 提取经过变换之后的信号: 小波域下的低频系数(近似信息)和高频系数(细节信号), 即"时域→小波域"!
    % 命令: appcoef低频系数提取; detcoef高频系数提取
    for i = 1:level 
        cDi = detcoef(C, L, i);
        % 多级重构系数: 从小波域还原出信号高频部分的子信号, 即从"小波域→时域"！
        Di = wrcoef('d', C, L, wavename, i);
        output_matrix = [output_matrix, Di];
    end  
    
    % 命令: wrcoef  参数中a是低频, d是高频
    cAi = appcoef(C, L, wavename, level);  % 低
    Ai = wrcoef('a', C, L, wavename, level); 
    output_matrix = [output_matrix, Ai];
    csvwrite('wavlet_result.csv', output_matrix);
    %output = output_matrix;
end