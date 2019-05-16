unzip(fullfile('data', 'data20190417232148.zip'), 'data');

files = [dir(fullfile('data', '*.gz')); dir(fullfile('data', '*.txt'))];
files = {files.name};

num_of_files = 0;
for i = 1:numel(files)
    file = strcat('data', filesep, files(i));
    [~,~,ext] = fileparts(file{1});
    if strcmp(ext, '.gz')
        num_of_files = num_of_files + 1;
    end
end

array_size = num_of_files  * 1440;

honx_array = cell(1, array_size);
hony_array = cell(1, array_size);
honz_array = cell(1, array_size);
hong_array = cell(1, array_size);

cell_pos = 1;

for i = 1:numel(files)
    file = strcat('data', filesep, files(i));
    [filepath,name,ext] = fileparts(file{1});
    if strcmp(ext, '.gz')
        extracted_files = gunzip(file);
        fileID = fopen(fullfile(filepath, name), 'r');
        while ~feof(fileID)
            tline = fgetl(fileID);
            if ~strcmp(tline(1), ' ') && ~strcmp(tline(1), 'D')
                values = split(tline);
                honx = values(4);
                hony = values(5);
                honz = values(6);
                hong = values(7);
                
                honx_array(1, cell_pos) = honx;
                hony_array(1, cell_pos) = hony;
                honz_array(1, cell_pos) = honz;
                hong_array(1, cell_pos) = hong;
                
                cell_pos = cell_pos + 1;
            end
        end
        fclose(fileID);
        delete(extracted_files{1});
    end
end

for k = 1:numel(files)
    delete(['data' filesep files{k}]);
end
