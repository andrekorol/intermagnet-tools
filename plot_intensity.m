unzip(fullfile('data', 'data20190417232148.zip'), 'data');
data = dir(fullfile('data', '*.gz'));
fields = fieldnames(data);
for i = 1:numel(fieldnames(data))
    disp(data(i).name);
end
files = [dir(fullfile('data', '*.gz')); dir(fullfile('data', '*.txt'))];
files = {files.name};
for k = 1:numel(files)
    delete(['data' filesep files{k}]);
end