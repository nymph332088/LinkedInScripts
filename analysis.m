uq1 = unique(studentInfo(:,4));
uq2 = unique(studentInfo(studentInfo(:,10)~=0,4));
num1 = hist(studentInfo(:,4),uq1);
num2 = hist(studentInfo(studentInfo(:,10)~=0,4), uq2);

ratios = [];
for i = 1:length(uq2)
    ratios(i) =num2(i)./num1(uq1==uq2(i));
end
%%
matched_students = studentInfo(studentInfo(:,10)~=0,:);
% matched_students = studentInfo;
c = matched_students(:,4);
uq = unique(c);
a = hist(c, uq);
[a, idx] = sort(a,'descend');
uq = uq(idx);
ratios = ratios(idx);
labels = {};
for i = 1:length(uq)
    ind = find(major_ids==uq(i));
    if(isempty(ind))
        labels{i} = 'Unknown';
    else
        labels{i} = major_names{ind};
    end
end


bar(a)
% for i = 1:length(a)
%     text(i,a(i)+1, num2str(ratios(i)))
% end
% Set the X-Tick locations so that every other month is labeled.
Xt = 1:length(a);
Xl = [0 length(a)];
set(gca,'XTick',Xt,'XLim',Xl);
% ax = axis;    % Current axis limits
% axis(axis);    % Set the axis limit modes (e.g. XLimMode) to manual
% Yl = ax(3:4);  % Y-axis limits
% % Place the text labels
% t = text(Xt,Yl(1)*ones(1,length(Xt)),labels);
% set(t,'HorizontalAlignment','right','VerticalAlignment','top', ...
%       'Rotation',45);
% % Remove the default labels
% set(gca,'XTickLabel','')
set(gca,'XTickLabel',labels);
rotateXLabels(gca,45);
ylabel('Number of Students');


%%
